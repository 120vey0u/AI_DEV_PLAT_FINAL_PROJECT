# 🎭 Sentiment Analysis AI System

[![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-blue.svg)](#)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](#)
[![Backend](https://img.shields.io/badge/API-FastAPI-009688.svg)](#)
[![Frontend](https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg)](#)
[![Database](https://img.shields.io/badge/DB-PostgreSQL-336791.svg)](#)

Một ứng dụng phân tích cảm xúc văn bản toàn diện (End-to-End AI Application). Dự án tích hợp mô hình xử lý ngôn ngữ tự nhiên (NLP) qua API, đóng gói bằng Docker, tự động hóa 배포 (CI/CD) qua GitHub Actions và lưu trữ dữ liệu bền vững trên PostgreSQL.

## 📑 Mục lục
- [Kiến trúc Hệ thống](#-kiến-trúc-hệ-thống)
- [Cấu trúc Thư mục](#-cấu-trúc-thư-mục)
- [Yêu cầu Môi trường](#-yêu-cầu-môi-trường)
- [Hướng dẫn Cài đặt & Chạy Local](#-hướng-dẫn-cài-đặt--chạy-local)
- [Triển khai với Docker](#-triển-khai-với-docker)
- [Quy trình CI/CD](#-quy-trình-cicd)
- [Thành viên Nhóm](#-thành-viên-nhóm)

---

## 🏗 Kiến trúc Hệ thống

Hệ thống được thiết kế theo mô hình Microservices tinh gọn, tách biệt hoàn toàn giữa UI, API logic và Database.

```mermaid
flowchart LR
    Client([Người dùng]) -->|HTTPS| UI(Streamlit Frontend)
    UI -->|REST API - JSON| API(FastAPI Backend)
    API <-->|Request/Response| HF[Hugging Face LLM API]
    API -->|Log (Text, Sentiment, Time)| DB[(PostgreSQL)]
```

---

## 📂 Cấu trúc Thư mục

```text
.
├── frontend/                 # Giao diện người dùng
│   ├── app.py                # Logic Streamlit UI
│   └── requirements.txt      # Dependencies cho frontend
├── backend/                  # API Server
│   ├── main.py               # Logic xử lý API FastAPI
│   └── requirements.txt      # Dependencies cho backend
├── database/                 # Lưu trữ Database Scripts
│   └── schema.sql            # Script khởi tạo bảng PostgreSQL
├── .github/workflows/        # Cấu hình CI/CD
│   └── deploy.yml            # Pipeline GitHub Actions
├── Dockerfile                # File đóng gói image cho toàn bộ ứng dụng
├── .gitignore                # Danh sách file ẩn/bỏ qua khi commit Git
└── README.md                 # Tài liệu dự án
```

---

## ⚙️ Yêu cầu Môi trường

Để chạy dự án này trên máy tính cá nhân, bạn cần cài đặt:
- **Python:** Phiên bản 3.9 trở lên.
- **Git:** Để quản lý mã nguồn.
- **Docker & Docker Compose:** (Tùy chọn) Nếu muốn chạy qua container.
- **PostgreSQL:** Cục bộ hoặc sử dụng Cloud DB (Supabase/Aiven).

---

## 🚀 Hướng dẫn Cài đặt & Chạy Local

### 1. Clone repository và thiết lập biến môi trường

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
cd YOUR-REPO-NAME
```

Tạo file `.env` ở thư mục gốc (tham khảo `.env.example` nếu có) để chứa các khóa bảo mật:
```env
# Database Config
DATABASE_URL=postgresql://user:password@host:port/dbname

# AI API Config
HUGGINGFACE_API_KEY=your_api_key_here
```

### 2. Khởi chạy Backend (FastAPI)

Mở một Terminal mới và thực thi tuần tự:
```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
📍 *Swagger UI API Docs có sẵn tại: `http://localhost:8000/docs`*

### 3. Khởi chạy Frontend (Streamlit)

Mở Terminal thứ 2 và thực thi tuần tự:
```bash
cd frontend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
📍 *Giao diện Web truy cập tại: `http://localhost:8501`*

---

## 🐳 Triển khai với Docker

Nếu bạn đã cài đặt Docker, bạn có thể build và chạy toàn bộ hệ thống bằng 2 lệnh duy nhất mà không cần cài đặt Python hay thư viện cục bộ:

```bash
# 1. Build Docker Image
docker build -t sentiment-ai-app .

# 2. Chạy Container với các cổng tương ứng và load biến môi trường
docker run -d -p 8000:8000 -p 8501:8501 --env-file .env --name sentiment_container sentiment-ai-app
```

---

## 🔄 Quy trình CI/CD

Dự án này sử dụng **GitHub Actions** để tự động hóa toàn bộ vòng đời phân phối phần mềm:

1. **Push/Merge vào nhánh `main`**: Kích hoạt Pipeline tự động.
2. **Test & Lint**: Kiểm tra lỗi cú pháp và chạy các Unit Test (nếu có).
3. **Build & Push Docker Image**: Đóng gói mã nguồn thành Docker Image và đẩy lên **Docker Hub**.
4. **Deploy**: Tự động kéo Image mới nhất từ Docker Hub về Server (Koyeb/Render) và khởi động lại dịch vụ thông qua Public HTTPS.

---

## 👥 Thành viên Nhóm & Trách nhiệm

| STT | Vị trí | Người phụ trách | Mô tả công việc (Deliverables) |
|:---:|:---|:---|:---|
| 1 | **AI & Backend Core** | `DuongP` | Viết FastAPI, tích hợp LLM/Hugging Face xử lý phân tích cảm xúc. |
| 2 | **PostgreSQL & Data** | `Huyen Anh` | Thiết kế schema DB, viết query SQL, cấu hình Cloud Database. |
| 3 | **DevOps (Docker)** | `Duc Duong` | Viết Dockerfile tối ưu, xử lý môi trường, push image lên Docker Hub. |
| 4 | **CI/CD & Deployment**| `Tu Vu` | Viết Github Actions workflow, cấu hình server triển khai HTTPS public. |
| 5 | **Frontend & Git Master** | `DuongVu` | Code Streamlit UI, quản lý Git/Merge conflict, viết hệ thống tài liệu. |

---
*Dự án thuộc Đồ án môn học Ứng dụng AI & Quá trình triển khai phần mềm (Git · Docker · CI/CD).*
