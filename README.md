# Text Sentiment Analysis

A web application for Vietnamese text sentiment analysis. The React frontend sends text to a FastAPI backend, which uses Gemini to identify sentiment and aspects, then stores the analysis history in PostgreSQL.

## Architecture

| Component | Technology | Hosting |
|---|---|---|
| Frontend | React, Vite, Tailwind CSS, Recharts | Vercel |
| Backend API | Python, FastAPI, SQLAlchemy | Render |
| Database | PostgreSQL | Supabase |
| AI | Gemini API (`gemini-3.5-flash-lite`) | Google AI API |
| CI/CD | GitHub Actions | GitHub |
| Container | Docker | Docker Hub |

```mermaid
flowchart TD
    U[User] -->|HTTPS| V["Vercel - React frontend"]
    V -->|REST API / JSON| R["Render - FastAPI backend"]
    R <-->|Prompt / response| G["Gemini API"]
    R -->|Read / write history| S[("Supabase - PostgreSQL")]
```

The frontend calls the backend, not Gemini directly. Keep the Gemini API key on the backend.

## Requirements

- Python 3.10+
- Node.js 20+ and npm
- PostgreSQL locally or a Supabase PostgreSQL database
- Gemini API key
- Git
- Docker and Docker Compose (optional, for containerized backend)

## 1. Clone the repository

```bash
git clone https://github.com/120vey0u/AI_DEV_PLAT_FINAL_PROJECT.git
cd AI_DEV_PLAT_FINAL_PROJECT
```

## 2. Set up PostgreSQL

Create a PostgreSQL database. Then create the application table using the repository schema.

For a local PostgreSQL server:

```bash
psql "postgresql://user:password@localhost:5432/dbname" -f database/schema.sql
```

Replace the username, password, port, and database name with your own values.

For Supabase, open **SQL Editor** in your project and run the contents of [database/schema.sql](database/schema.sql).

The table stores the submitted text, the JSONB analysis result, and its creation timestamp.

## 3. Configure the backend

Create `backend/.env`:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
GEMINI_API_KEY=your_gemini_api_key
```

For Supabase, use the PostgreSQL connection string provided by Supabase as `DATABASE_URL`.

The backend requires `DATABASE_URL` and `GEMINI_API_KEY`. Do not put the Gemini key in frontend configuration or commit real credentials to Git.

## 4. Install and run the backend

From the repository root:

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

Backend URLs:

- Health check: [http://localhost:8000/health](http://localhost:8000/health)
- Interactive API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

Keep this terminal running.

## 5. Install and run the frontend

Open a second terminal at the repository root:

```bash
cd frontend
npm ci
```

Create `frontend/.env.local`:

```env
VITE_API_URL=http://localhost:8000
```

Start Vite:

```bash
npm run dev
```

Open the local URL printed by Vite (normally [http://localhost:5173](http://localhost:5173)).

## Run the backend with Docker

The Dockerfile packages **the FastAPI backend only**. The frontend and PostgreSQL database run separately.

Create a `.env` file in the repository root:

```env
PORT=8000
DATABASE_URL=postgresql://user:password@host.docker.internal:5432/dbname
GEMINI_API_KEY=your_gemini_api_key
```

When PostgreSQL runs directly on the host machine, use `host.docker.internal` instead of `localhost` from inside the container. The connection string format is:

```text
postgresql://user:password@host.docker.internal:port/dbname
```

If PostgreSQL runs in another container, use that container's service name on the same Docker network. If using Supabase, use the Supabase connection string instead.

On Linux, if `host.docker.internal` does not resolve, add this under the `backend` service in `docker-compose.yml`:

```yaml
extra_hosts:
  - "host.docker.internal:host-gateway"
```

Build and start:

```bash
docker compose up --build -d
docker compose logs -f backend
```

Stop:

```bash
docker compose down
```

## Deploy the system

Production uses **Supabase** for PostgreSQL, **Render** for FastAPI, and **Vercel** for React.

### 1. Supabase — database

1. Create a PostgreSQL project.
2. Run [database/schema.sql](database/schema.sql) in the SQL Editor.
3. Copy the database connection string. Keep it private.

### 2. Render — backend

Create a Render **Web Service** connected to this repository:

- Runtime: **Docker**
- Root Directory: repository root
- Dockerfile Path: `./Dockerfile`
- Health Check Path: `/health`

Add these environment variables in Render:

```env
DATABASE_URL=<your-supabase-postgresql-connection-string>
GEMINI_API_KEY=<your-gemini-api-key>
```

The Dockerfile uses Render's `PORT` variable to start Uvicorn. After deployment, verify that `https://<your-render-service>.onrender.com/health` returns:

```json
{"status":"ok"}
```

### 3. Vercel — frontend

Connect the repository to Vercel and use the **repository root** as the project root. The root `vercel.json` is used by the GitHub Actions deployment workflow to build the frontend from `frontend/package.json`.

Set this environment variable in Vercel:

```env
VITE_API_URL=https://<your-render-service>.onrender.com
```

Deploy the project, open the Vercel URL, and test a text analysis.

### 4. CORS configuration

The backend currently allows:

- `https://sentimentanalysis-kappa.vercel.app`
- `http://localhost:5173`
- `http://localhost:3000`

If the Vercel domain changes, update `allow_origins` in [backend/main.py](backend/main.py) with the exact frontend origin and redeploy the backend.

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Backend health check |
| POST | `/api/v1/analyze` | Analyze text and save the result |
| GET | `/api/v1/history` | List analysis history |
| GET | `/api/v1/history/{history_id}` | Get one history record |
| DELETE | `/api/v1/history/{history_id}` | Delete one history record |

Example request:

```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \\
  -H "Content-Type: application/json" \\
  -d '{"text":"Dịch vụ tốt, nhân viên thân thiện nhưng giá hơi cao."}'
```

## CI/CD

The workflow is defined in [\.github/workflows/ci-cd.yml](.github/workflows/ci-cd.yml). It runs on pushes and pull requests targeting `main`.

The current pipeline:

1. Starts PostgreSQL and checks the database schema.
2. Installs backend dependencies and runs backend tests.
3. Installs frontend dependencies and builds the React app.
4. Builds and pushes the backend Docker image to Docker Hub.
5. Deploys the frontend using the Vercel CLI.

Add these GitHub Actions **Secrets** for the corresponding steps:

- `DOCKER_USERNAME`
- `DOCKER_PASSWORD`
- `VERCEL_TOKEN`
- `VERCEL_ORG_ID`
- `VERCEL_PROJECT_ID`
- `DATABASE_URL` (optional; used by the Supabase connectivity check)

Render and Supabase are configured in their own dashboards.

> **Important:** Some checks in the current workflow use `|| echo`, which can hide a test, build, or database-check failure and still allow the job to succeed. A green run is not a reliable pass signal until those commands are changed to return a failing exit code.

## Security

- Never commit `.env`, `.env.local`, database passwords, or API keys.
- Keep `GEMINI_API_KEY` on the backend only.
- Use separate credentials for development and production.
- If a credential has been committed to a public repository, rotate it. Removing it from the latest file does not remove it from Git history.
