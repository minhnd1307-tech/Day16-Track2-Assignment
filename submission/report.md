1. Tôi dùng Google Cloud Platform (GCP), region us-central1 / zone us-central1-a, instance type e2-medium (2 vCPU, 4GB RAM), source commit 55539f6.
2. Dataset Credit Card Fraud Detection có 284,807 dòng và 31 đặc trưng, chia train/test theo tỷ lệ 80/20 có phân tầng (stratify=y), random_state 42.
3. Load dữ liệu mất 3.314 giây; training mất 7.8432 giây; best iteration là 0 (100 rounds boosting).
4. AUC-ROC 0.9466, Accuracy 0.9992, F1-Score 0.7565, Precision 0.7684, Recall 0.7449 trên tập test.
5. Latency 1 dòng trung bình 0.7328 ms; throughput batch 1.000 dòng đạt 239,317.64 dòng/giây; đo bằng time.perf_counter().
6. CPU/RAM/Network tôi quan sát lúc benchmark xong là CPU 0.0% us, RAM 537.1 MiB used / 3924.7 MiB total (14%), load average 0.12; ảnh đính kèm screenshots/02_resource_monitoring_top.png.
7. Billing tại ngày 01-02/10/2026 ghi nhận 78 VNĐ (tiết kiệm 78 VNĐ, chi phí thực trả 0 VNĐ); ảnh đính kèm screenshots/03_gcp_billing.png.
8. Tôi đã tải kết quả và cấu hình dọn dẹp tài nguyên (terraform destroy) lúc kết thúc thực hành; bằng chứng terminal và file kết quả lưu tại screenshots/01_benchmark_terminal.png và benchmark_result.json.
