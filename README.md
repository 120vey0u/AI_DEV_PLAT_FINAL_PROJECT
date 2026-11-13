# Text Sentiment Analysis

Ứng dụng phân tích cảm xúc văn bản tiếng Việt. Người dùng nhập văn bản trên giao diện React; frontend gửi yêu cầu đến backend FastAPI. Backend sử dụng Gemini API để phân tích cảm xúc và các khía cạnh được đề cập, sau đó lưu kết quả vào PostgreSQL.

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

Frontend không gọi Gemini trực tiếp. Gemini API key được lưu và sử dụng ở backend.

## Yêu cầu môi trường

- Git và Gemini API key.
- **Chạy không sử dụng Docker:** Python 3.10 trở lên, Node.js 20 trở lên và npm, PostgreSQL local hoặc PostgreSQL trên Supabase.
- **Chạy bằng Docker Compose:** Docker Engine và Docker Compose v2. Không cần cài Python, Node.js hoặc PostgreSQL trực tiếp trên máy host vì các thành phần này chạy trong container.

## Tải mã nguồn

```bash
git clone https://github.com/120vey0u/AI_DEV_PLAT_FINAL_PROJECT.git
cd AI_DEV_PLAT_FINAL_PROJECT
```

## Chạy ứng dụng

Có hai cách chạy ứng dụng: cài đặt và khởi chạy từng thành phần trực tiếp trên máy, hoặc sử dụng Docker Compose để chạy frontend, backend và database trong các container.

### A. Chạy không sử dụng Docker

Ở cách này, frontend và backend chạy trực tiếp trên máy bằng Node.js và Python. PostgreSQL có thể chạy trên máy local hoặc sử dụng Supabase.

#### Bước 1. Chuẩn bị PostgreSQL

Tạo một database PostgreSQL, sau đó khởi tạo bảng bằng file schema:

```bash
psql "postgresql://user:password@localhost:5432/dbname" -f database/schema.sql
```

Thay `user`, `password`, `port` và `dbname` bằng thông tin database của bạn.

Nếu sử dụng Supabase, mở **SQL Editor** trong dự án Supabase và chạy nội dung file [database/schema.sql](database/schema.sql). Sao chép PostgreSQL connection string để sử dụng ở bước cấu hình backend.

Bảng `sentiment_history` lưu văn bản đầu vào, kết quả phân tích dạng JSONB và thời điểm tạo bản ghi.

#### Bước 2. Cấu hình và chạy Backend

Tạo file `backend/.env`:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
GEMINI_API_KEY=your_gemini_api_key
```

Khi sử dụng Supabase, thay giá trị `DATABASE_URL` bằng connection string do Supabase cung cấp.

Mở terminal tại thư mục gốc repository và chạy:

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

Backend cung cấp các địa chỉ:

- Health check: [http://localhost:8000/health](http://localhost:8000/health)
- API documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

Giữ terminal backend hoạt động trong khi sử dụng ứng dụng.

#### Bước 3. Cài đặt và chạy Frontend riêng

Frontend được cài đặt và chạy độc lập trong terminal thứ hai.

```bash
cd frontend
npm ci
```

Tạo file `frontend/.env.local`:

```env
VITE_API_URL=http://localhost:8000
```

Khởi chạy Vite development server:

```bash
npm run dev
```

Truy cập địa chỉ được hiển thị trong terminal (mặc định là [http://localhost:5173](http://localhost:5173)).

Frontend cần backend hoạt động tại `http://localhost:8000` để gửi yêu cầu phân tích. PostgreSQL cũng phải sẵn sàng và được cấu hình đúng trong `backend/.env`.

### B. Chạy bằng Docker Compose

File `docker-compose.yml` định nghĩa ba service: `frontend`, `backend` và `db`. **Mỗi service được chạy trong một container riêng.** Docker Compose quản lý vòng đời và mạng kết nối của cả ba container.

Khi chạy `docker compose up --build -d`, Compose build image cho frontend và backend (PostgreSQL sử dụng image `postgres:15-alpine`), sau đó tạo và khởi chạy ba container tương ứng. Đây không phải là một container duy nhất chứa cả ứng dụng.

| Service | Container | Vai trò | Port trên máy host |
|---|---|---|
| `frontend` | `sentiment_frontend` | React/Vite development server | `3000` |
| `backend` | `sentiment_backend` | FastAPI REST API | `8000` |
| `db` | `sentiment_db` | PostgreSQL 15 | `5432` |

#### Bước 1. Cấu hình biến môi trường

Tạo file `.env` tại thư mục gốc repository:

```env
PORT=8000
DATABASE_URL=postgresql://postgres:postgres@db:5432/sentiment_db
GEMINI_API_KEY=your_gemini_api_key
```

Các lưu ý về cấu hình:

- Hostname `db` là tên service PostgreSQL trong Docker network. Backend chạy trong container phải dùng `db`, không dùng `localhost`, để kết nối tới database.
- Connection string phải khớp với các giá trị `POSTGRES_DB`, `POSTGRES_USER` và `POSTGRES_PASSWORD` được khai báo trong service `db` của `docker-compose.yml`.
- `GEMINI_API_KEY` được backend sử dụng để gọi Gemini API.
- File `.env` chứa thông tin nhạy cảm và không được commit lên Git.

#### Bước 2. Build và khởi chạy các container

Chạy lệnh tại thư mục gốc repository:

```bash
docker compose up --build -d
```

Docker Compose thực hiện các công việc:

1. Tạo và khởi chạy container `sentiment_db` từ image PostgreSQL 15; kiểm tra trạng thái database bằng health check.
2. Build backend image từ `./Dockerfile`, sau đó khởi chạy container `sentiment_backend` khi database đã healthy.
3. Build frontend image từ `frontend/Dockerfile` và khởi chạy container `sentiment_frontend`.

Sau lệnh này, cả ba container đều do Docker Compose quản lý. Không cần chạy thêm lệnh `docker run` để khởi động frontend.

#### Bước 3. Truy cập ứng dụng

Kiểm tra các container đang chạy:

```bash
docker compose ps
```

Kết quả sẽ hiển thị ba service/container `frontend`, `backend` và `db`.

Sau khi các container khởi động thành công:

- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend health check: [http://localhost:8000/health](http://localhost:8000/health)
- API documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
- PostgreSQL: `localhost:5432` (kết nối từ công cụ database trên máy host).

Frontend trong Compose gửi yêu cầu đến `http://localhost:8000`. Đây là địa chỉ API mà trình duyệt trên máy host truy cập; không thay bằng hostname nội bộ `backend` trong cấu hình `VITE_API_URL`.

#### Bước 4. Theo dõi và dừng các container

```bash
# Xem trạng thái container
docker compose ps

# Theo dõi log của các service
docker compose logs -f frontend backend db

# Dừng và xóa container, giữ lại dữ liệu PostgreSQL
docker compose down
```

PostgreSQL sử dụng named volume `postgres_data` để lưu dữ liệu. File `database/schema.sql` được mount vào thư mục khởi tạo của PostgreSQL và tự động chạy khi database volume được khởi tạo lần đầu.

**Lưu ý:** Lệnh `docker compose down -v` xóa cả volume `postgres_data` và dữ liệu database local. Chỉ sử dụng lệnh này khi cần reset database.

Trong cấu hình Docker Compose tiêu chuẩn, frontend đã là một service và được chạy trong container `sentiment_frontend` cùng với backend và database. Không cần build hoặc khởi chạy frontend bằng một lệnh Docker riêng.

Nếu muốn phát triển frontend trực tiếp trên máy host thay vì dùng frontend container, hãy sử dụng hướng dẫn ở mục **A. Chạy không sử dụng Docker** cho frontend và đặt `VITE_API_URL=http://localhost:8000`. Khi đó có thể chỉ khởi chạy database và backend bằng:

```bash
docker compose up --build -d db backend
```

Đây là cách chạy kết hợp tùy chọn dành cho phát triển, không phải bước bổ sung bắt buộc của Docker Compose.

## Triển khai hệ thống

Môi trường production sử dụng **Supabase** cho PostgreSQL, **Render** cho FastAPI và **Vercel** cho React.

### 1. Supabase — Cơ sở dữ liệu

1. Tạo một dự án PostgreSQL trên Supabase.
2. Mở SQL Editor và chạy file [database/schema.sql](database/schema.sql).
3. Sao chép PostgreSQL connection string và lưu trữ an toàn.

### 2. Render — Backend

Tạo một **Web Service** trên Render và kết nối với repository GitHub.

Cấu hình dịch vụ:

- Runtime: **Docker**
- Root Directory: thư mục gốc repository.
- Dockerfile Path: `./Dockerfile`
- Health Check Path: `/health`

Thêm các biến môi trường trong phần Environment của Render:

```env
DATABASE_URL=<your-supabase-postgresql-connection-string>
GEMINI_API_KEY=<your-gemini-api-key>
```

Dockerfile sử dụng biến `PORT` do Render cung cấp để khởi chạy Uvicorn. Sau khi deploy, kiểm tra địa chỉ `https://<your-render-service>.onrender.com/health`. Kết quả mong đợi:

```json
{"status":"ok"}
```

### 3. Vercel — Frontend

Kết nối repository với Vercel và sử dụng thư mục gốc repository làm Project Root. File `vercel.json` ở thư mục gốc định nghĩa cấu hình build frontend từ `frontend/package.json`.

Thiết lập biến môi trường trong Vercel:

```env
VITE_API_URL=https://<your-render-service>.onrender.com
```

Deploy project và truy cập domain Vercel để kiểm tra chức năng phân tích văn bản.

### 4. Cấu hình CORS

Backend cho phép các origin sau:

- `https://sentimentanalysis-kappa.vercel.app`
- `http://localhost:5173`
- `http://localhost:3000`

Khi sử dụng domain frontend khác, bổ sung chính xác origin đó vào danh sách `allow_origins` trong [backend/main.py](backend/main.py), sau đó deploy lại backend.

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

Workflow CI/CD được định nghĩa trong file [.github/workflows/ci-cd.yml](.github/workflows/ci-cd.yml) và kích hoạt khi có `push` hoặc `pull request` hướng đến nhánh `main`.

Các bước chính:

1. Khởi chạy PostgreSQL và kiểm tra schema database.
2. Cài đặt dependencies của backend và chạy backend tests.
3. Cài đặt dependencies của frontend và build ứng dụng React.
4. Build backend Docker image và push lên Docker Hub khi có push lên nhánh `main`.
5. Deploy frontend bằng Vercel CLI khi có push lên nhánh `main`.

Các GitHub Actions **Secrets** cần cấu hình:

- `DOCKER_USERNAME`
- `DOCKER_PASSWORD`
- `VERCEL_TOKEN`
- `VERCEL_ORG_ID`
- `VERCEL_PROJECT_ID`
- `DATABASE_URL` — PostgreSQL connection string của Supabase, dùng trong bước kiểm tra kết nối database.

Render và Supabase được cấu hình riêng trong dashboard của từng nền tảng. Workflow build và push backend image lên Docker Hub; việc triển khai backend trên Render được quản lý theo cấu hình của Render.

## Bảo mật

- Không commit các file `.env`, `.env.local`, mật khẩu database hoặc API key.
- Chỉ sử dụng `GEMINI_API_KEY` ở backend.
- Các tài khoản mặc định trong Docker Compose dành cho môi trường local. Thay đổi thông tin xác thực trước khi sử dụng trong môi trường chia sẻ hoặc production.
- Sử dụng thông tin đăng nhập riêng cho môi trường development và production.
- Nếu thông tin đăng nhập bị lộ hoặc từng được commit lên repository công khai, hãy thay đổi (rotate) thông tin đó. Xóa khỏi file mới nhất không đồng nghĩa với việc xóa khỏi Git history.
