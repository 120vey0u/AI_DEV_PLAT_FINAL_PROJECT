INSERT INTO sentiment_history (input_text, analysis_data) VALUES 
(
    'Phong cảnh nơi đây thật sự thanh tịnh và đẹp đẽ, tuy nhiên tiếng gió rít đôi lúc hơi ồn ào và đáng sợ.', 
    '{
      "overall": "Đan xen",
      "highlightedText": [
        {
          "text": "Phong cảnh nơi đây thật sự ",
          "sentiment": "neutral"
        },
        {
          "text": "thanh tịnh và đẹp đẽ",
          "sentiment": "positive"
        },
        {
          "text": ", tuy nhiên tiếng gió rít đôi lúc hơi ",
          "sentiment": "neutral"
        },
        {
          "text": "ồn ào và đáng sợ",
          "sentiment": "negative"
        },
        {
          "text": ".",
          "sentiment": "neutral"
        }
      ],
      "aspects": [
        {
          "name": "Cảnh quan",
          "score": 95,
          "sentiment": "positive"
        },
        {
          "name": "Âm thanh",
          "score": 50,
          "sentiment": "negative"
        }
      ]
    }'::jsonb
),
(
    'Sản phẩm dùng rất tuyệt vời, giao hàng nhanh chóng!', 
    '{
      "overall": "Tích cực",
      "highlightedText": [
        {"text": "Sản phẩm dùng rất tuyệt vời", "sentiment": "positive"},
        {"text": ", giao hàng nhanh chóng!", "sentiment": "positive"}
      ],
      "aspects": [
        {"name": "Chất lượng", "score": 95, "sentiment": "positive"},
        {"name": "Giao hàng", "score": 90, "sentiment": "positive"}
      ]
    }'::jsonb
),
(
    'Dịch vụ chăm sóc khách hàng quá tệ, thất vọng toàn tập.', 
    '{
      "overall": "Tiêu cực",
      "highlightedText": [
        {"text": "Dịch vụ chăm sóc khách hàng quá tệ", "sentiment": "negative"},
        {"text": ", thất vọng toàn tập.", "sentiment": "negative"}
      ],
      "aspects": [
        {"name": "CSKH", "score": 10, "sentiment": "negative"}
      ]
    }'::jsonb
),
(
    'Ứng dụng tạm ổn, cần cải thiện thêm giao diện cho bắt mắt hơn.', 
    '{
      "overall": "Trung lập",
      "highlightedText": [
        {"text": "Ứng dụng tạm ổn", "sentiment": "neutral"},
        {"text": ", cần cải thiện thêm giao diện cho bắt mắt hơn.", "sentiment": "neutral"}
      ],
      "aspects": [
        {"name": "Giao diện", "score": 50, "sentiment": "neutral"}
      ]
    }'::jsonb
),
(
    'Chất lượng âm thanh nghe rất hay và ấm, tuy nhiên pin lại hơi nhanh hết.', 
    '{
      "overall": "Đan xen",
      "highlightedText": [
        {"text": "Chất lượng âm thanh nghe rất hay và ấm", "sentiment": "positive"},
        {"text": ", tuy nhiên pin lại hơi nhanh hết.", "sentiment": "negative"}
      ],
      "aspects": [
        {"name": "Âm thanh", "score": 88, "sentiment": "positive"},
        {"name": "Pin", "score": 40, "sentiment": "negative"}
      ]
    }'::jsonb
),
(
    'Món ăn ngon, giá rẻ bất ngờ nhưng không gian quán hơi chật chội.', 
    '{
      "overall": "Đan xen",
      "highlightedText": [
        {"text": "Món ăn ngon, giá rẻ bất ngờ", "sentiment": "positive"},
        {"text": " nhưng không gian quán hơi chật chội.", "sentiment": "negative"}
      ],
      "aspects": [
        {"name": "Món ăn & Giá", "score": 92, "sentiment": "positive"},
        {"name": "Không gian", "score": 35, "sentiment": "negative"}
      ]
    }'::jsonb
),
(
    'Nhân viên thân thiện, cửa hàng sạch sẽ, mọi thứ đều rất hoàn hảo.', 
    '{
      "overall": "Tích cực",
      "highlightedText": [
        {"text": "Nhân viên thân thiện, cửa hàng sạch sẽ, mọi thứ đều rất hoàn hảo.", "sentiment": "positive"}
      ],
      "aspects": [
        {"name": "Nhân viên", "score": 98, "sentiment": "positive"},
        {"name": "Vệ sinh", "score": 95, "sentiment": "positive"}
      ]
    }'::jsonb
),
(
    'Đóng gói hàng hóa cực kỳ cẩu thả khiến sản phẩm bị móp méo bên trong.', 
    '{
      "overall": "Tiêu cực",
      "highlightedText": [
        {"text": "Đóng gói hàng hóa cực kỳ cẩu thả khiến sản phẩm bị móp méo bên trong.", "sentiment": "negative"}
      ],
      "aspects": [
        {"name": "Đóng gói", "score": 15, "sentiment": "negative"}
      ]
    }'::jsonb
);

