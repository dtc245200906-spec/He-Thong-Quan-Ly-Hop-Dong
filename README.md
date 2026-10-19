# HỆ THỐNG QUẢN LÝ HỢP ĐỒNG

## 1. Giới thiệu
Dự án xây dựng hệ thống quản lý hợp đồng bằng Python Flask, kết hợp giám sát hệ thống bằng Prometheus và Grafana.

## 2. Công nghệ sử dụng
- Python, Flask
- Docker và Docker Compose
- Prometheus
- Grafana
- Node Exporter
- Git và GitHub

## 3. Chức năng
- Quản lý danh sách hợp đồng.
- Thêm và chỉnh sửa thông tin hợp đồng.
- Theo dõi trạng thái hợp đồng.
- Cung cấp endpoint kiểm tra sức khỏe ứng dụng (`/health`).
- Cung cấp số liệu giám sát (`/metrics`).
- Theo dõi các chỉ số hệ thống qua Grafana.

## 4. Cấu trúc dự án
```text
contract-management-monitoring/
├── app/
│   ├── app.py
│   └── templates/
│       ├── index.html
│       └── edit.html
├── prometheus/
│   └── prometheus.yml
├── docker-compose.yml
├── requirements.txt
└── .gitignore
```

## 5. Hướng dẫn chạy
Chạy ứng dụng Flask trong môi trường Python đã cài đặt các thư viện từ `requirements.txt`.

Khởi động hệ thống giám sát bằng lệnh:

```bash
docker compose up -d
```

Các địa chỉ truy cập khi chạy trên máy cá nhân:

- Ứng dụng Flask: http://localhost:5000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001

## 6. Kết quả
- Xây dựng giao diện quản lý hợp đồng.
- Tích hợp Prometheus để thu thập số liệu.
- Thiết lập Grafana Dashboard với 4 biểu đồ giám sát.
- Sử dụng Docker Compose để quản lý các dịch vụ giám sát.
