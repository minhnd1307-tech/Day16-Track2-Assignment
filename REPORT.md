# BÁO CÁO THỰC HÀNH LAB 16: CLOUD AI ENVIRONMENT SETUP (GCP)

**Học viên:** Nguyễn Đức Minh  
**Môi trường:** Google Cloud Platform (GCP) - `us-central1-a`  
**Hạ tầng:** 
- Máy ảo: Compute Engine `e2-medium` (2 vCPU, 4GB RAM), chạy Debian 12
- Mạng: Private VPC, Cloud Router + Cloud NAT (Egress-only), kết nối bảo mật qua Google Identity-Aware Proxy (IAP)
- Thuật toán: LightGBM (Gradient Boosting Decision Tree)
- Bộ dữ liệu: Credit Card Fraud Detection (284,807 dòng, 31 đặc trưng)

---

## 1. Kết quả Benchmark Mô hình

| Chỉ số (Metric) | Kết quả đo được | Đánh giá & Ý nghĩa thực tế |
|---|---|---|
| **Thời gian nạp dữ liệu (Load Time)** | **3.31 giây** | Tải và parse toàn bộ 284,807 dòng CSV vào pandas DataFrame rất nhanh trên ổ đĩa SSD GCP. |
| **Thời gian huấn luyện (Training Time)** | **7.84 giây** | Thuật toán LightGBM tận dụng cơ chế Histogram-based binning giúp huấn luyện 100 cây quyết định trên CPU chỉ dưới 8 giây mà không cần GPU đắt tiền. |
| **AUC-ROC** | **0.9466** (94.66%) | Khả năng phân tách giữa giao dịch gian lận và bình thường rất cao trên tập dữ liệu mất cân bằng nghiêm trọng (chỉ 0.17% gian lận). |
| **Accuracy** | **0.9992** (99.92%) | Tỷ lệ chính xác tổng thể đạt gần như tuyệt đối. |
| **Precision** | **0.7684** (76.84%) | Trong số các giao dịch bị mô hình cảnh báo gian lận, có gần 77% là gian lận thực tế, hạn chế báo động giả làm phiền khách hàng. |
| **Recall** | **0.7449** (74.49%) | Bắt được gần 75% các hành vi gian lận thực tế xảy ra trong hệ thống. |
| **F1-Score** | **0.7565** | Trung bình điều hòa giữa Precision và Recall đạt mức cân bằng tốt. |
| **Inference Latency (1 dòng)** | **0.7328 ms** (< 1ms) | Độ trễ cực thấp (< 1 mili-giây), hoàn toàn đáp ứng chuẩn thời gian thực (Real-time scoring) cho các máy thanh toán thẻ tín dụng (POS). |
| **Inference Throughput (1000 dòng)** | **239,317 QPS** | Khả năng suy luận lô (Batch inference) đạt hơn 239 nghìn giao dịch mỗi giây trên 2 vCPU, tối ưu tuyệt vời cho xử lý đối soát cuối ngày. |

---

## 2. Đánh giá Giám sát Tài nguyên & Chi phí (FinOps)

1. **Hiệu năng CPU & RAM (quan sát từ `top`):**
   - Bộ nhớ RAM tiêu thụ lúc vận hành chỉ khoảng **537 MiB / 3.8 GiB** (chiếm ~14%), lượng bộ nhớ còn trống rất dồi dào (~2.5 GiB free + 1 GiB cache), không xảy ra tình trạng thiếu thốn bộ nhớ hay Swapping.
   - CPU `e2-medium` chịu tải tốt, tải trung bình (load average: 0.12) ở mức rất thấp và an toàn.

2. **Tối ưu chi phí (GCP Billing):**
   - Chi phí phát sinh thực tế chỉ khoảng **78 VNĐ** (~$0.003), gần như bằng 0 nhờ triển khai luồng CPU tinh gọn, không phát sinh chi phí GPU ($0.35/h) hay chi phí máy ảo trung chuyển Bastion Host ($0.03/h).
   - Kiến trúc sử dụng **Cloud NAT + IAP TCP Forwarding** vừa đảm bảo tiêu chuẩn bảo mật Private Subnet (không lộ Public IP của Compute Node), vừa tiết kiệm tối đa ngân sách vận hành.

---

## 3. Danh mục Deliverables đính kèm trong mã nguồn

1. **Terminal chạy Benchmark:** [screenshots/01_benchmark_terminal.png](screenshots/01_benchmark_terminal.png)
2. **Giám sát tài nguyên máy ảo (top):** [screenshots/02_resource_monitoring_top.png](screenshots/02_resource_monitoring_top.png)
3. **Báo cáo chi phí Google Cloud Billing:** [screenshots/03_gcp_billing.png](screenshots/03_gcp_billing.png)
4. **Dữ liệu số liệu Benchmark đầy đủ:** [benchmark_result.json](benchmark_result.json)
5. **Mã nguồn kịch bản benchmark:** [benchmark.py](benchmark.py)
6. **Mã nguồn Terraform triển khai GCP:** [terraform-gcp/](terraform-gcp/)
