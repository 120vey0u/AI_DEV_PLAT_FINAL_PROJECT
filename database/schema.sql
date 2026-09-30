CREATE TABLE IF NOT EXISTS sentiment_history (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100),                 -- ID người dùng thực hiện
    input_text TEXT NOT NULL,             -- Nội dung văn bản đầu vào
    sentiment_result VARCHAR(50) NOT NULL, -- Kết quả phân tích (Positive, Negative, Neutral)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tạo Index tối ưu tốc độ tìm kiếm theo thời gian và theo người dùng
CREATE INDEX IF NOT EXISTS idx_sentiment_created_at ON sentiment_history(created_at);
CREATE INDEX IF NOT EXISTS idx_sentiment_user_id ON sentiment_history(user_id);