import time
import json
import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score, f1_score, precision_score, recall_score

print("=== STARTING LIGHTGBM BENCHMARK ON GCP CPU NODE ===")

# 1. Load Data
t0 = time.time()
df = pd.read_csv("creditcard.csv")
load_time = time.time() - t0
print(f"1. Data loaded in {load_time:.2f} seconds. Shape: {df.shape}")

# 2. Preprocess & Split
X = df.drop(columns=['Class'])
y = df['Class']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 3. Train Model
train_data = lgb.Dataset(X_train, label=y_train)
valid_data = lgb.Dataset(X_test, label=y_test, reference=train_data)

params = {
    'objective': 'binary',
    'metric': 'auc',
    'boosting_type': 'gbdt',
    'learning_rate': 0.05,
    'num_leaves': 31,
    'verbose': -1,
    'n_jobs': -1
}

t_train_start = time.time()
evals_result = {}
model = lgb.train(
    params,
    train_data,
    num_boost_round=100,
    valid_sets=[train_data, valid_data],
    callbacks=[lgb.record_evaluation(evals_result)]
)
train_time = time.time() - t_train_start
print(f"2. Training completed in {train_time:.2f} seconds.")

# 4. Evaluation
y_pred_proba = model.predict(X_test, num_iteration=model.best_iteration)
y_pred_binary = (y_pred_proba >= 0.5).astype(int)

auc = float(roc_auc_score(y_test, y_pred_proba))
acc = float(accuracy_score(y_test, y_pred_binary))
f1 = float(f1_score(y_test, y_pred_binary))
prec = float(precision_score(y_test, y_pred_binary))
rec = float(recall_score(y_test, y_pred_binary))

# 5. Measure Inference Latency & Throughput
single_row = X_test.iloc[0:1]
latencies = []
for _ in range(50):
    t_start = time.perf_counter()
    _ = model.predict(single_row)
    latencies.append((time.perf_counter() - t_start) * 1000)
latency_ms = float(np.mean(latencies))

thousand_rows = X_test.iloc[0:1000]
t_start_batch = time.perf_counter()
_ = model.predict(thousand_rows)
batch_time_s = time.perf_counter() - t_start_batch
throughput_qps = float(1000.0 / batch_time_s)

results = {
    "load_time_sec": round(load_time, 4),
    "train_time_sec": round(train_time, 4),
    "best_iteration": model.best_iteration,
    "auc_roc": round(auc, 4),
    "accuracy": round(acc, 4),
    "f1_score": round(f1, 4),
    "precision": round(prec, 4),
    "recall": round(rec, 4),
    "inference_latency_single_row_ms": round(latency_ms, 4),
    "inference_throughput_1000_rows_qps": round(throughput_qps, 2)
}

print("\n=== BENCHMARK RESULTS ===")
print(json.dumps(results, indent=2))

with open("benchmark_result.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nSaved output to benchmark_result.json successfully!")
