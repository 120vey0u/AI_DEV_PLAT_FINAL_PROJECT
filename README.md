# Text Sentiment Analysis

Ứng dụng phân tích cảm xúc văn bản tiếng Việt. Frontend React gửi văn bản đến backend FastAPI. Backend sử dụng Gemini để phân tích cảm xúc và các khía cạnh được đề cập, sau đó lưu lịch sử phân tích vào PostgreSQL.

## Kiến trúc hệ thống

| Thành phần | Công nghệ | Nền tảng triển khai |
|---|---|---|
| Frontend | React, Vite, Tailwind CSS, Recharts | Vercel |
| Backend API | Python, FastAPI, SQLAlchemy | Render |
| Cơ sở dữ liệu | PostgreSQL | Supabase |
| AI | Gemini API (`gemini-3.5-flash-lite`) | Google AI API |
| CI/CD | GitHub Actions | GitHub |
| Đóng gói ứng dụng | Docker | Docker Hub |

```mermaid
flowchart TD
    U[Người dùng] -->|HTTPS| V["Vercel - React frontend"]
    V -->|REST API / JSON| R["Render - FastAPI backend"]
    R <-->|Prompt / phản hồi| G["Gemini API"]
    R -->|Đọc / ghi lịch sử| S[("Supabase - PostgreSQL")]
```

Frontend không gọi Gemini trực tiếp. API key của Gemini chỉ được lưu và sử dụng ở backend.

## Yêu cầu môi trường

- Python 3.10 trở lên.
- Node.js 20 trở lên và npm.
- PostgreSQL cài trên máy hoặc cơ sở dữ liệu PostgreSQL trên Supabase.
- Gemini API key.
- Git.
- Docker và Docker Compose (tùy chọn, dùng để chạy toàn bộ hệ thống trong container).

## 1. Tải mã nguồn

```bash
git clone https://github.com/120vey0u/AI_DEV_PLAT_FINAL_PROJECT.git
cd AI_DEV_PLAT_FINAL_PROJECT
```

## 2. Thiết lập PostgreSQL

Tạo một database PostgreSQL. Sau đó tạo bảng lưu lịch sử phân tích bằng schema có sẵn trong repository.

Nếu sử dụng PostgreSQL trên máy cá nhân:

```bash
psql "postgresql://user:password@localhost:5432/dbname" -f database/schema.sql
```

Thay tên người dùng, mật khẩu, port và tên database bằng thông tin thực tế của bạn.

Nếu sử dụng Supabase, mở **SQL Editor** trong dự án Supabase và chạy nội dung file [database/schema.sql](database/schema.sql).

Bảng `sentiment_history` lưu văn bản đầu vào, kết quả phân tích dạng JSONB và thời điểm tạo bản ghi.

## 3. Cấu hình Backend

Tạo file `backend/.env`:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
GEMINI_API_KEY=your_gemini_api_key
```

Nếu sử dụng Supabase, đặt connection string PostgreSQL do Supabase cung cấp vào biến `DATABASE_URL`.

Backend yêu cầu hai biến môi trường `DATABASE_URL` và `GEMINI_API_KEY`. Không đặt Gemini API key trong cấu hình frontend và không commit thông tin đăng nhập thật lên Git.

## 4. Cài đặt và chạy Backend

Tại thư mục gốc của repository, mở terminal và thực hiện:

```bash
cd backend
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows PowerShell
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Sau khi khởi chạy, backend có các địa chỉ:

- Kiểm tra trạng thái: [http://localhost:8000/health](http://localhost:8000/health)
- Tài liệu API tương tác: [http://localhost:8000/docs](http://localhost:8000/docs)

Giữ terminal này hoạt động trong suốt quá trình sử dụng.

## 5. Cài đặt và chạy Frontend

Mở terminal thứ hai tại thư mục gốc repository:

```bash
cd frontend
npm ci
```

Tạo file `frontend/.env.local`:

```env
VITE_API_URL=http://localhost:8000
```

Khởi chạy Vite:

```bash
npm run dev
```

Mở địa chỉ local được hiển thị trong terminal (mặc định là [http://localhost:5173](http://localhost:5173)).

## Chạy toàn bộ hệ thống bằng Docker Compose

File `docker-compose.yml` hiện cấu hình **3 service**: PostgreSQL (`db`), FastAPI (`backend`) và React/Vite (`frontend`). Vì vậy, chạy Docker Compose sẽ khởi động cả frontend lẫn database, không chỉ riêng backend.

### 1. Cấu hình biến môi trường

Tạo file `.env` tại thư mục gốc repository:

```env
PORT=8000
DATABASE_URL=postgresql://postgres:postgres@db:5432/sentiment_db
GEMINI_API_KEY=your_gemini_api_key
```

Giải thích:

- `DATABASE_URL` dùng hostname `db` vì backend kết nối tới PostgreSQL thông qua tên service trong Docker network. Không dùng `localhost` ở đây.
- Tên database, username và password trong connection string phải khớp với cấu hình `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` của service `db` trong `docker-compose.yml`. Hiện tại các giá trị local mặc định đều là `sentiment_db` và `postgres`.
- `GEMINI_API_KEY` là API key dùng bởi backend.
- File `.env` đã được Git ignore; không commit file này lên repository.

### 2. Build và khởi chạy

Chạy lệnh tại thư mục gốc:

```bash
docker compose up --build -d
```

Docker Compose sẽ:

1. Khởi chạy PostgreSQL 15 và kiểm tra trạng thái database bằng health check.
2. Chờ database sẵn sàng rồi khởi chạy backend FastAPI.
3. Build và khởi chạy frontend bằng Dockerfile trong thư mục `frontend/`.

### 3. Các service và địa chỉ truy cập

| Service | Vai trò | Port trên máy host |
|---|---|---|
| `frontend` | Giao diện React chạy bằng Vite | `3000` |
| `backend` | FastAPI REST API | `8000` |
| `db` | PostgreSQL 15 | `5432` |

Sau khi các container khởi động thành công:

- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend health check: [http://localhost:8000/health](http://localhost:8000/health)
- API documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
- PostgreSQL: `localhost:5432` (kết nối từ công cụ database trên máy host).

Trong cấu hình Compose hiện tại, frontend gọi API qua `http://localhost:8000`. Đây là địa chỉ mà trình duyệt của người dùng truy cập; không thay bằng hostname nội bộ `backend` trong biến `VITE_API_URL`.

### 4. Theo dõi và dừng hệ thống

```bash
# Xem trạng thái các container
docker compose ps

# Theo dõi log của cả 3 service
docker compose logs -f frontend backend db

# Dừng và xóa các container, giữ lại dữ liệu PostgreSQL
docker compose down
```

PostgreSQL sử dụng named volume `postgres_data` để lưu dữ liệu. File `database/schema.sql` được mount vào thư mục khởi tạo của PostgreSQL và chỉ tự động chạy khi volume database được tạo lần đầu.

**Lưu ý:** `docker compose down -v` sẽ xóa cả volume `postgres_data`, đồng nghĩa với việc xóa dữ liệu database local. Chỉ chạy lệnh này khi bạn thực sự muốn reset database.

## Chạy Frontend riêng

Có thể chạy frontend độc lập với Docker Compose hoặc chạy frontend trong một container riêng. Trong cả hai trường hợp, backend API vẫn phải được khởi động và truy cập được tại `http://localhost:8000`.

### Cách 1: Chạy frontend trực tiếp bằng Node.js

Trước tiên, dùng Docker Compose để chỉ khởi động database và backend:

```bash
docker compose up --build -d db backend
```

Sau đó, mở terminal mới và chạy frontend trên máy host:

```bash
cd frontend
npm ci
```

Tạo file `.env.local` trong thư mục `frontend/`:

```env
VITE_API_URL=http://localhost:8000
```

Khởi động frontend:

```bash
npm run dev
```

Truy cập [http://localhost:5173](http://localhost:5173). Backend được cung cấp bởi container và frontend chạy trực tiếp bằng Node.js.

### Cách 2: Build và chạy frontend trong container riêng

Đảm bảo backend và database đang chạy, sau đó build image frontend tại thư mục gốc:

```bash
docker compose up --build -d db backend
docker build -t sentiment-frontend ./frontend
```

Chạy frontend container:

```bash
docker run --rm --name sentiment-frontend \
  -p 3000:3000 \
  -e VITE_API_URL=http://localhost:8000 \
  sentiment-frontend
```

Truy cập [http://localhost:3000](http://localhost:3000).

**Lưu ý:** `frontend/Dockerfile` hiện chạy Vite development server (`npm run dev`), phù hợp cho development và kiểm thử. Frontend production hiện được build và triển khai riêng trên Vercel.

## Triển khai hệ thống

Môi trường production sử dụng **Supabase** cho PostgreSQL, **Render** cho FastAPI và **Vercel** cho React.

### 1. Supabase — Cơ sở dữ liệu

1. Tạo một dự án PostgreSQL trên Supabase.
2. Mở SQL Editor và chạy file [database/schema.sql](database/schema.sql).
3. Sao chép PostgreSQL connection string. Giữ thông tin này ở chế độ riêng tư.

### 2. Render — Backend

Tạo một **Web Service** trên Render và kết nối với repository GitHub này.

Cấu hình dịch vụ:

- Runtime: **Docker**
- Root Directory: thư mục gốc repository.
- Dockerfile Path: `./Dockerfile`
- Health Check Path: `/health`

Thêm các biến môi trường sau trong phần Environment của Render:

```env
DATABASE_URL=<your-supabase-postgresql-connection-string>
GEMINI_API_KEY=<your-gemini-api-key>
```

Dockerfile sử dụng biến `PORT` do Render cung cấp để khởi chạy Uvicorn. Sau khi deploy, kiểm tra địa chỉ `https://<your-render-service>.onrender.com/health`. Kết quả mong đợi:

```json
{"status":"ok"}
```

### 3. Vercel — Frontend

Kết nối repository với Vercel và sử dụng **thư mục gốc repository** làm Project Root. File `vercel.json` ở thư mục gốc được workflow GitHub Actions sử dụng để build frontend từ `frontend/package.json`.

Thiết lập biến môi trường sau trong Vercel:

```env
VITE_API_URL=https://<your-render-service>.onrender.com
```

Deploy project, mở địa chỉ Vercel và thử phân tích một đoạn văn bản.

### 4. Cấu hình CORS

Backend hiện cho phép các origin sau:

- `https://sentimentanalysis-kappa.vercel.app`
- `http://localhost:5173`
- `http://localhost:3000`

Nếu domain Vercel thay đổi, cập nhật danh sách `allow_origins` trong [backend/main.py](backend/main.py) với chính xác frontend origin mới, sau đó deploy lại backend.

## API endpoints

| Phương thức | Endpoint | Mô tả |
|---|---|---|
| GET | `/health` | Kiểm tra trạng thái backend |
| POST | `/api/v1/analyze` | Phân tích văn bản và lưu kết quả |
| GET | `/api/v1/history` | Lấy danh sách lịch sử phân tích |
| GET | `/api/v1/history/{history_id}` | Lấy một bản ghi lịch sử |
| DELETE | `/api/v1/history/{history_id}` | Xóa một bản ghi lịch sử |

Ví dụ gọi API:

```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text":"Dịch vụ tốt, nhân viên thân thiện nhưng giá hơi cao."}'
```

## CI/CD

Workflow được cấu hình trong file [\.github/workflows/ci-cd.yml](.github/workflows/ci-cd.yml). Workflow được kích hoạt khi có `push` hoặc `pull request` hướng đến nhánh `main`.

Các bước chính trong pipeline hiện tại:

1. Khởi chạy PostgreSQL và kiểm tra schema database.
2. Cài đặt dependencies của backend và chạy backend tests.
3. Cài đặt dependencies của frontend và build ứng dụng React.
4. Build backend Docker image và push lên Docker Hub (chỉ khi push lên nhánh `main`).
5. Deploy frontend bằng Vercel CLI (chỉ khi push lên nhánh `main`).

Thêm các GitHub Actions **Secrets** sau để workflow hoạt động:

- `DOCKER_USERNAME`
- `DOCKER_PASSWORD`
- `VERCEL_TOKEN`
- `VERCEL_ORG_ID`
- `VERCEL_PROJECT_ID`
- `DATABASE_URL` — connection string của Supabase, được sử dụng ở bước kiểm tra kết nối database trong workflow hiện tại.

Render và Supabase được cấu hình riêng trong dashboard của từng nền tảng. Backend image được build và push lên Docker Hub; bước deploy Render được quản lý riêng theo cấu hình của Render.

## Bảo mật

- Không commit các file `.env`, `.env.local`, mật khẩu database hoặc API key.
- Chỉ sử dụng `GEMINI_API_KEY` ở backend.
- Các tài khoản mặc định trong Docker Compose chỉ dành cho môi trường local; hãy thay đổi trước khi sử dụng trong môi trường chia sẻ hoặc production.
- Sử dụng thông tin đăng nhập riêng cho môi trường development và production.
- Nếu thông tin đăng nhập từng được commit lên repository công khai, hãy đổi (rotate) thông tin đó. Xóa khỏi file mới nhất không đồng nghĩa với việc xóa khỏi Git history.
