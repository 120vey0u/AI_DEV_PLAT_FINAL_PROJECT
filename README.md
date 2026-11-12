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
- Docker và Docker Compose (không bắt buộc, dùng khi muốn chạy backend bằng container).

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

## Chạy Backend bằng Docker

Dockerfile hiện tại chỉ đóng gói **backend FastAPI**. Frontend và PostgreSQL được chạy như các thành phần riêng biệt.

Tạo file `.env` tại thư mục gốc repository:

```env
PORT=8000
DATABASE_URL=postgresql://user:password@host.docker.internal:5432/dbname
GEMINI_API_KEY=your_gemini_api_key
```

Khi PostgreSQL chạy trực tiếp trên máy host, backend bên trong container cần dùng `host.docker.internal` thay cho `localhost`. Cấu trúc connection string:

```text
postgresql://user:password@host.docker.internal:port/dbname
```

Nếu PostgreSQL chạy trong một container khác, hãy sử dụng tên service của container đó trên cùng Docker network. Nếu sử dụng Supabase, hãy dùng connection string do Supabase cung cấp.

Trên Linux, nếu `host.docker.internal` không phân giải được, thêm cấu hình sau vào service `backend` trong file `docker-compose.yml`:

```yaml
extra_hosts:
  - "host.docker.internal:host-gateway"
```

Build và khởi chạy:

```bash
docker compose up --build -d
docker compose logs -f backend
```

Dừng container:

```bash
docker compose down
```

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
curl -X POST "http://localhost:8000/api/v1/analyze" \\
  -H "Content-Type: application/json" \\
  -d '{"text":"Dịch vụ tốt, nhân viên thân thiện nhưng giá hơi cao."}'
```

## CI/CD

Workflow được cấu hình trong file [\.github/workflows/ci-cd.yml](.github/workflows/ci-cd.yml). Workflow được kích hoạt khi có `push` hoặc `pull request` hướng đến nhánh `main`.

Các bước chính trong pipeline hiện tại:

1. Khởi chạy PostgreSQL và kiểm tra schema database.
2. Cài đặt dependencies của backend và chạy backend tests.
3. Cài đặt dependencies của frontend và build ứng dụng React.
4. Build backend Docker image và push lên Docker Hub.
5. Deploy frontend bằng Vercel CLI.

Thêm các GitHub Actions **Secrets** sau để các bước tương ứng có thể hoạt động:

- `DOCKER_USERNAME`
- `DOCKER_PASSWORD`
- `VERCEL_TOKEN`
- `VERCEL_ORG_ID`
- `VERCEL_PROJECT_ID`
- `DATABASE_URL` (không bắt buộc; dùng cho bước kiểm tra kết nối Supabase)

Render và Supabase được cấu hình riêng trong dashboard của từng nền tảng.

> **Lưu ý:** Một số lệnh kiểm tra trong workflow hiện tại sử dụng `|| echo`. Cách viết này có thể che giấu lỗi test, build hoặc kiểm tra database, khiến job vẫn được đánh dấu thành công. Vì vậy, trạng thái workflow màu xanh chưa đảm bảo tất cả kiểm tra đều vượt qua cho đến khi các lệnh này được sửa để trả về exit code lỗi khi thất bại.

## Bảo mật

- Không commit các file `.env`, `.env.local`, mật khẩu database hoặc API key.
- Chỉ sử dụng `GEMINI_API_KEY` ở backend.
- Sử dụng thông tin đăng nhập riêng cho môi trường development và production.
- Nếu thông tin đăng nhập từng được commit lên repository công khai, hãy đổi (rotate) thông tin đó. Xóa khỏi file mới nhất không đồng nghĩa với việc xóa khỏi Git history.
