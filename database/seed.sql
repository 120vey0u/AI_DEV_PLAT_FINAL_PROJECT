-- Dữ liệu mẫu (Data Seed) cho bảng sentiment_history
INSERT INTO sentiment_history (user_id, input_text, sentiment_result, sentiment_type) VALUES
('user_001', 'Sản phẩm dùng rất tuyệt vời, giao hàng nhanh chóng!', 'Positive', 'Product Review'),
('user_002', 'Dịch vụ chăm sóc khách hàng quá tệ, thất vọng.', 'Negative', 'Customer Service'),
('user_003', 'Ứng dụng tạm ổn, cần cải thiện thêm giao diện.', 'Neutral', 'General Feedback');