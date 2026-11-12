# Text Sentiment Analysis

[![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-blue.svg)](.github/workflows/ci-cd.yml)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](Dockerfile)
[![Frontend](https://img.shields.io/badge/Frontend-React-61DAFB.svg)](frontend/)
[![Backend](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](backend/)
[![Database](https://img.shields.io/badge/Database-PostgreSQL-336791.svg)](database/)

**Text Sentiment Analysis** là ứng dụng phân tích cảm xúc văn bản sử dụng mô hình Gemini. Người dùng nhập một đoạn văn bản trên giao diện React; backend FastAPI gửi nội dung đến Gemini API, nhận kết quả phân tích theo từng khía cạnh, lưu lịch sử vào PostgreSQL và trả kết quả về frontend để trực quan hóa.

- **GitHub Repository:** [120vey0u/AI_DEV_PLAT_FINAL_PROJECT](https://github.com/120vey0u/AI_DEV_PLAT_FINAL_PROJECT)
- **Frontend:** ReactJS + Vite — triển khai trên Vercel.
- **Backend:** Python + FastAPI — triển khai trên Render.
- **Database:** PostgreSQL — triển khai trên Supabase.
- **LLM:** Gemini API.

## 📑 Mục lục

- [Tổng quan kiến trúc](#-tổng-quan-kiến-trúc)
- [Luồng xử lý](#-luồng-xử-lý)
- [Cấu trúc thư mục](#-cấu-trúc-thư-mục)
- [Công nghệ sử dụng](#-công-nghệ-sử-dụng)
- [Yêu cầu môi trường](#-yêu-cầu-môi-trường)
- [Cài đặt và chạy Local không dùng Docker](#-cài-đặt-và-chạy-local-không-dùng-docker)
- [Chạy Backend bằng Docker](#-chạy-backend-bằng-docker)
- [Triển khai và cấu hình môi trường](#-triển-khai-và-cấu-hình-môi-trường)
- [CI/CD với GitHub Actions](#-cicd-với-github-actions)
- [Phân công nhiệm vụ](#-phân-công-nhiệm-vụ)

---

## 🏗 Tổng quan kiến trúc

Dự án sử dụng kiến trúc tách biệt frontend, backend và database. Ba thành phần được triển khai trên các nền tảng tương ứng:

| Thành phần | Công nghệ | Nền tảng triển khai |
|---|---|---|
| Frontend | ReactJS, Vite | **Vercel** |
| Backend API | Python, FastAPI | **Render** |
| Database | PostgreSQL | **Supabase** |
| AI / LLM | Gemini API | Google AI API |
| Container | Docker | Docker Hub |
| CI/CD | GitHub Actions | GitHub |

### Sơ đồ kiến trúc triển khai

```mermaid
flowchart TD
    U[Người dùng] -->|HTTPS| V["Vercel - ReactJS Frontend"]
    V -->|REST API / JSON| R["Render - FastAPI Backend"]
    R <-->|Prompt / JSON response| G[Gemini API]
    R -->|SQL query / save history| S["Supabase - PostgreSQL"]
```

Frontend không gọi Gemini trực tiếp. Mọi yêu cầu phân tích đều đi qua FastAPI để bảo vệ API key và tập trung xử lý nghiệp vụ ở backend.

## 🔄 Luồng xử lý

1. Người dùng nhập văn bản và nhấn **Analyze** trên giao diện React.
2. Frontend gửi HTTP POST request đến endpoint `/api/v1/analyze` của FastAPI.
3. Backend gọi Gemini API để phân tích cảm xúc tổng quan, các đoạn văn và những khía cạnh (aspects) được đề cập.
4. Backend lưu văn bản đầu vào cùng dữ liệu phân tích vào bảng `sentiment_history` trong PostgreSQL.
5. FastAPI trả JSON response về frontend.
6. React hiển thị kết quả, phần văn bản được tô màu theo cảm xúc và biểu đồ điểm số các khía cạnh.

Các endpoint chính:

| Method | Endpoint | Chức năng |
|---|---|---|
| GET | `/health` | Kiểm tra trạng thái backend |
| POST | `/api/v1/analyze` | Phân tích văn bản và lưu lịch sử |
| GET | `/api/v1/history` | Lấy danh sách lịch sử |
| GET | `/api/v1/history/{history_id}` | Lấy một bản ghi lịch sử |
| DELETE | `/api/v1/history/{history_id}` | Xóa một bản ghi lịch sử |

Khi chạy backend local, có thể xem tài liệu API tại [http://localhost:8000/docs](http://localhost:8000/docs).

## 📂 Cấu trúc thư mục

```text
AI_DEV_PLAT_FINAL_PROJECT/
├── .github/
│   └── workflows/
│       └── ci-cd.yml             # GitHub Actions pipeline
├── backend/
│   ├── app/
│   │   ├── ai/
│   │   │   └── gemini_client.py  # Gọi Gemini API
│   │   ├── core/
│   │   │   └── config.py         # Đọc cấu hình và biến môi trường
│   │   ├── database/
│   │   │   ├── crud.py           # Các thao tác dữ liệu
│   │   │   ├── models.py         # SQLAlchemy model
│   │   │   └── session.py        # Kết nối PostgreSQL
│   │   ├── routers/
│   │   │   └── sentiment.py      # Các API endpoint
│   │   └── services/
│   │       └── sentiment_service.py
│   ├── tests/                    # Backend tests
│   ├── main.py                   # Khởi tạo FastAPI
│   ├── requirements.txt
│   └── .env.example              # Mẫu biến môi trường
├── database/
│   ├── schema.sql                # Database schema
│   ├── seed.sql                  # Dữ liệu mẫu
│   └── setup-guide.md
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── App.jsx               # Giao diện và xử lý tương tác
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── Dockerfile                    # Đóng gói Backend FastAPI
├── docker-compose.yml            # Chạy Backend container
├── vercel.json
└── README.md
```

## 🧰 Công nghệ sử dụng

| Hạng mục | Công nghệ / Công cụ |
|---|---|
| Ngôn ngữ và framework backend | Python, FastAPI |
| Frontend | ReactJS, Vite, Tailwind CSS |
| Trực quan hóa | Recharts |
| Cơ sở dữ liệu | PostgreSQL, SQLAlchemy |
| Mô hình ngôn ngữ | Gemini API — model `gemini-3.5-flash-lite` |
| DevOps | Git, Docker, Docker Hub |
| CI/CD | GitHub Actions |
| Triển khai frontend | Vercel |
| Triển khai backend | Render |
| Database hosting | Supabase |

## ⚙️ Yêu cầu môi trường

Để chạy dự án trên máy cá nhân, cần chuẩn bị:

- **Python 3.10+** và pip.
- **Node.js 20+** và npm.
- **PostgreSQL** (cài local) hoặc tài khoản Supabase.
- **Gemini API key**.
- **Git**.
- **Docker và Docker Compose** nếu muốn chạy backend bằng container.

## 🚀 Cài đặt và chạy Local không dùng Docker

Phần này hướng dẫn chạy frontend và backend trực tiếp trên máy tính, không cần Docker.

### 1. Clone repository

```bash
git clone https://github.com/120vey0u/AI_DEV_PLAT_FINAL_PROJECT.git
cd AI_DEV_PLAT_FINAL_PROJECT
```

### 2. Tạo database và bảng PostgreSQL

Tạo một database PostgreSQL, ví dụ `dbname`, cùng user/password tương ứng. Sau đó kết nối vào database bằng pgAdmin, DBeaver hoặc `psql` và chạy câu lệnh sau để tạo bảng lưu lịch sử phân tích:

```sql
CREATE TABLE sentiment_history (
    id SERIAL PRIMARY KEY,
    input_text TEXT NOT NULL,
    analysis_data JSON NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

> Nếu sử dụng Supabase thay vì PostgreSQL cài trên máy, mở **SQL Editor** của Supabase và chạy cùng câu lệnh trên database của dự án.

### 3. Tạo file ENV cho Backend

Backend đọc hai biến môi trường bắt buộc là `DATABASE_URL` và `GEMINI_API_KEY`. Tạo file **`backend/.env`** (nằm cùng cấp với `main.py`) với nội dung:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
GEMINI_API_KEY=your_gemini_api_key
```

Thay `user`, `password`, `5432`, `dbname` và `your_gemini_api_key` bằng thông tin thực tế. Với PostgreSQL local, cấu trúc connection string là:

```text
postgresql://user:password@localhost:port/dbname
```

**Lưu ý:** Dự án hiện sử dụng `GEMINI_API_KEY`; không cần khai báo `HUGGINGFACE_API_KEY`.

### 4. Cài đặt và khởi chạy Backend

Mở terminal tại thư mục gốc dự án:

```bash
cd backend
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows PowerShell: .venv\Scripts\Activate.ps1

pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Backend chạy tại `http://localhost:8000`.

- Health check: [http://localhost:8000/health](http://localhost:8000/health)
- API documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

### 5. Cài đặt và khởi chạy Frontend

Mở terminal thứ hai tại thư mục gốc dự án:

```bash
cd frontend
npm install
```

Tạo file **`frontend/.env.local`** để frontend biết địa chỉ backend:

```env
VITE_API_URL=http://localhost:8000
```

Sau đó chạy:

```bash
npm run dev
```

Truy cập địa chỉ Vite hiển thị trên terminal, mặc định là [http://localhost:5173](http://localhost:5173).

## 🐳 Chạy Backend bằng Docker

Dockerfile hiện tại đóng gói **Backend FastAPI**. Frontend ReactJS được chạy/deploy riêng; PostgreSQL cũng là dịch vụ riêng, không được tạo tự động bởi Dockerfile hiện tại.

### 1. Tạo file ENV ở thư mục gốc

Khi chạy bằng Docker Compose hoặc `docker run`, tạo file **`.env` tại thư mục gốc repository**:

```env
PORT=8000
DATABASE_URL=postgresql://user:password@host.docker.internal:5432/dbname
GEMINI_API_KEY=your_gemini_api_key
```

Khi backend chạy trong container và PostgreSQL chạy trực tiếp trên máy host, cần dùng `host.docker.internal` thay cho `localhost`. Cấu trúc connection string:

```text
postgresql://user:password@host.docker.internal:port/dbname
```

- `localhost` bên trong container trỏ về chính container, không phải máy host.
- Nếu PostgreSQL chạy trong một container/dịch vụ khác, hãy dùng hostname của dịch vụ đó trên cùng Docker network.
- Nếu dùng Supabase, hãy sử dụng connection string do Supabase cung cấp thay vì địa chỉ `host.docker.internal`.
- Trên Linux, nếu Docker Engine không phân giải được `host.docker.internal`, thêm cấu hình sau vào service backend trong `docker-compose.yml`:

```yaml
extra_hosts:
  - "host.docker.internal:host-gateway"
```

### 2. Chạy bằng Docker Compose

```bash
docker compose up --build -d
```

Kiểm tra container:

```bash
docker compose ps
docker compose logs -f backend
```

Dừng container:

```bash
docker compose down
```

### 3. Hoặc build và chạy bằng Docker CLI

```bash
docker build -t sentiment-analysis-backend .
docker run -d --name sentiment-backend -p 8000:8000 --env-file .env sentiment-analysis-backend
```

Backend sẽ được expose tại port 8000 của máy host.

## ☁️ Triển khai và cấu hình môi trường

Dự án được triển khai theo mô hình frontend, backend và database trên ba nền tảng riêng biệt.

### 1. Frontend — Vercel

- Import repository vào Vercel và chọn thư mục frontend là project root (Root Directory: `frontend`).
- Build command: `npm run build`.
- Output directory: `dist`.
- Thiết lập Environment Variable:

```env
VITE_API_URL=https://<your-render-service>.onrender.com
```

Thay URL mẫu bằng public URL backend thực tế trên Render.

### 2. Backend — Render

Triển khai backend FastAPI trên Render bằng Dockerfile ở thư mục gốc repository. Cấu hình các Environment Variables trên Render:

```env
DATABASE_URL=<supabase-postgresql-connection-string>
GEMINI_API_KEY=<your-gemini-api-key>
```

Render cấp port cho web service qua biến môi trường `PORT`; ứng dụng sử dụng biến này khi khởi động trong container. Không đưa Gemini API key vào frontend hoặc commit key lên GitHub.

### 3. Database — Supabase

- Tạo PostgreSQL project trên Supabase.
- Chạy câu lệnh tạo bảng `sentiment_history` trong SQL Editor.
- Lấy PostgreSQL connection string trong phần kết nối database của Supabase.
- Đặt connection string đó làm giá trị `DATABASE_URL` trong Environment Variables của Render.

Không commit file `.env`, mật khẩu database hoặc API key lên repository.

## 🔄 CI/CD với GitHub Actions

Workflow được cấu hình tại `.github/workflows/ci-cd.yml` và được kích hoạt khi có `push` hoặc `pull_request` vào nhánh `main`.

Các công việc chính trong pipeline:

1. **Kiểm tra Backend và Database:** thiết lập PostgreSQL test service, kiểm tra schema và cài đặt môi trường Python để chạy backend tests.
2. **Kiểm tra Frontend:** cài dependencies và build ứng dụng React/Vite.
3. **Build và Push Docker Image:** đóng gói backend và đẩy image lên Docker Hub.
4. **Deploy Frontend:** sử dụng Vercel CLI để build và triển khai frontend lên Vercel.

Backend được host trên Render và database được host trên Supabase. Thông tin nhạy cảm phục vụ pipeline phải được lưu trong GitHub Actions Secrets, không ghi trực tiếp vào file workflow.

Các secrets được workflow tham chiếu gồm:

- `DOCKER_USERNAME`, `DOCKER_PASSWORD`
- `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`
- `DATABASE_URL` (nếu cần kiểm tra kết nối Supabase trong pipeline)

## 👥 Phân công nhiệm vụ

| STT | Mảng nhiệm vụ | Nhiệm vụ chi tiết | Deliverables | Người phụ trách | Mã sinh viên |
|:---:|---|---|---|---|---|
| 1 | **AI & Backend Core** | Xây dựng API bằng FastAPI; tích hợp Gemini API để phân tích cảm xúc và các khía cạnh của văn bản. | Backend API và logic phân tích hoạt động ổn định. | Phan Huy Dương | B25DCTN028 |
| 2 | **PostgreSQL & Data** | Thiết kế schema, quản lý bảng lưu lịch sử phân tích; cấu hình PostgreSQL trên Supabase. | PostgreSQL database hoạt động trên server. | Trần Huyền Anh | B25DCTN028 |
| 3 | **DevOps (Docker)** | Xây dựng Dockerfile, xử lý biến môi trường, build Docker image và push image lên Docker Hub. | Dockerfile và Docker image trên Docker Hub. | Nguyễn Đức Dương | B25DCTN02 |
| 4 | **CI/CD & Deployment** | Xây dựng GitHub Actions workflow để tự động hóa kiểm tra, build và deploy; cấu hình dịch vụ public HTTPS. | GitHub Actions workflow và các địa chỉ dịch vụ public HTTPS. | Vũ Tuấn Tú | B25DCTN134 |
| 5 | **Frontend, Git Master & Docs** | Phát triển giao diện ReactJS; quản lý repository, branch, pull request, merge conflict và tài liệu dự án. | Frontend, GitHub repository, pull request và README. | Vũ Ngọc Dương | B25DCTN030 |

---

*Dự án môn học Nền tảng phát triển Trí Tuệ Nhân Tạo.*
