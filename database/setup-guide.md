## Database Setup (PostgreSQL & Supabase)
1. **Cloud Database Provider**: Supabase (PostgreSQL Direct Connection)
2. **Table Schema (`sentiment_history`)**:
   - `id`: Serial (Primary Key)
   - `input_text`: Text (Not Null)
   - `sentiment_result`: Varchar(50) (Not Null)
   - `created_at`: Timestamp with time zone
3. **Connection String Environment Variable**:
   ```env
   DATABASE_URL=postgresql://postgres:finalproject2026AI@db.idtwosgqbwqqehbutsck.supabase.co:5432/postgres