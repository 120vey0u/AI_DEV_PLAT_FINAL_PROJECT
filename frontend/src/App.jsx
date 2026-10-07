import { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import PrimaryButton from './components/PrimaryButton';

function App() {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleAnalyze = () => {
    if (!text.trim()) return;
    setLoading(true);
    setResult(null);

    setTimeout(() => {
      setResult({
        overall: "Interwoven",
        highlightedText: [
          { text: "Phong cảnh nơi đây thật sự ", sentiment: "neutral" },
          { text: "thanh tịnh và đẹp đẽ", sentiment: "positive" },
          { text: ", tuy nhiên tiếng gió rít đôi lúc hơi ", sentiment: "neutral" },
          { text: "ồn ào và đáng sợ", sentiment: "negative" },
          { text: ".", sentiment: "neutral" }
        ],
        aspects: [
          { name: "Cảnh quan", score: 95, sentiment: "positive" },
          { name: "Âm thanh", score: 50, sentiment: "negative" }
        ]
      });
      setLoading(false);
    }, 2000);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-teal-950 via-emerald-900 to-green-950 p-8 flex flex-col justify-center relative overflow-hidden">
      <div className="max-w-2xl mx-auto p-10 rounded-2xl bg-white/10 backdrop-blur-xl border border-white/25 shadow-2xl">        
        {/* Tiêu đề dùng font Serif */}
        <h1 className="text-5xl font-serif text-center mb-8 bg-gradient-to-r from-yellow-200 via-yellow-400 to-yellow-500 bg-clip-text text-transparent animate-pulse [animation-duration:6s] drop-shadow-lg">
          Sentiment Analysis
        </h1>

        {/* Ô nhập liệu được làm tối màu, có hiệu ứng viền sáng lên khi bấm vào */}
        <textarea 
          placeholder="Type Your Paragraph...."
          rows="4"
          className="w-full p-4 rounded-xl bg-black/40 text-white placeholder-gray-400 border border-white/10 focus:outline-none focus:ring-2 focus:ring-green-500/50 resize-none transition-all"
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        {/* Nút bấm thiền tịnh (CSS đã được giấu gọn gàng sang file khác) */}
        <PrimaryButton onClick={handleAnalyze} disabled={loading}>
          {loading ? "Loading" : "Analyze"}
        </PrimaryButton>

        {/* Khu vực kết quả hiện ra sau khi phân tích */}
        {result && !loading && (
          <div className="mt-8 p-6 rounded-2xl bg-black/20 border border-white/5 backdrop-blur-md transition-all animate-in fade-in slide-in-from-bottom-4 duration-500">
            <h2 className="text-xs font-semibold text-white/40 uppercase tracking-[0.2em] mb-4">Dissection Results:</h2>

            {/* Box 1: Text Highlighting */}
            <div className="mb-6 p-4 rounded-xl bg-black/40 border border-white/5">
              <h3 className="text-white/40 text-xs uppercase tracking-widest mb-4">Details of the passage</h3>

              <p className="text-lg leading-loose font-light">
                {/* Lệnh map() để lặp qua từng mảnh chữ */}
                {result.highlightedText.map((item, index) => {

                  // Mặc định chữ màu trắng nhạt
                  let colorClass = "text-white/80";

                  // Nếu là lời khen -> Nền xanh, chữ xanh sáng
                  if (item.sentiment === "positive") {
                    colorClass = "italic bg-green-500/20 text-green-300 px-1.5 py-0.5 rounded-md font-bold border border-green-500/20";
                  }

                  // Nếu là lời chê -> Nền đỏ, chữ đỏ sáng
                  if (item.sentiment === "negative") {
                    colorClass = "italic bg-red-500/20 text-red-300 px-1.5 py-0.5 rounded-md font-bold border border-red-500/20";
                  }

                  return (
                    <span key={index} className={colorClass}>
                      {item.text}
                    </span>
                  );
                })}
              </p>
            </div>

            {/* Box 2: Biểu đồ thống kê (Recharts) */}
            <div className="mt-4 h-64 p-4 rounded-xl bg-black/40 border border-white/5">
              <h3 className="text-white/40 text-xs uppercase tracking-widest mb-4">Details of aspects</h3>

              <ResponsiveContainer width="100%" height="80%">
                {/* Đưa mảng result.aspects vào làm dữ liệu */}
                <BarChart data={result.aspects}>
                  {/* Trục ngang X hiển thị tên khía cạnh */}
                  <XAxis dataKey="name" stroke="#ffffff50" fontSize={12} tickLine={false} axisLine={false}/>

                  {/* Trục dọc Y (Ẩn đi cho thiết kế tối giản) */}
                  <YAxis hide domain={[0, 100]} />

                  {/* Hộp thoại nổi lên khi di chuột vào */}
                  <Tooltip 
                    cursor={{fill: '#ffffff10'}}
                    contentStyle={{backgroundColor: '#000000cc', borderColor: '#ffffff20', borderRadius: '8px', color: '#fff'}}
                  />

                  {/* Cột dữ liệu */}
                  <Bar dataKey="score" fill="#ffffff" radius={[6, 6, 6, 6]}>
                    {/* Quét qua dữ liệu, tốt thì tô màu xanh, xấu thì tô màu đỏ */}
                    {result.aspects.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.sentiment === 'positive' ? '#10b981' : '#ef4444'} />
                    ))}
                  </Bar>

                </BarChart>

              </ResponsiveContainer>
            </div>

            {/* Box 3: Câu chốt hạ (Kết luận tổng quan) */}
            {(() => {
              // 1. Tinh toan trung binh sentiment
              const totalScore = result.aspects.reduce((sum, item) => (sum + item.score), 0);
              const avgScore = totalScore / result.aspects.length;
              const isPositive = avgScore >= 50;

              // 2. Chot phan ket luan va mau sac
              const conclusionState = result.overall;
              const conclusionText = isPositive ? "Câu văn truyền tải những cảm xúc đan xen. Khung cảnh được miêu tả là yên bình và tuyệt đẹp, gợi lên cảm giác tích cực, trong khi tiếng gió ồn ào và đáng sợ lại mang đến cảm xúc tiêu cực. Nhìn chung, sắc thái cảm xúc ở đây có sự cân bằng giữa sự tán thưởng và cảm giác khó chịu." : "Overall, the paragraph is more negative.";
              
              // Tam thoi de mau state la mau vang, sau nay doi sau
              const colorClassState = "italic bg-yellow-500/20 text-yellow-300 px-1.5 py-0.5 rounded-md font-extrabold border border-yellow-500/20";
              
              const colorClassText = isPositive ? "bg-green-500/20 border-green-500/40 text-green-300" : "bg-red-500/20 border-red-500/40 text-red-300";

              // 3. Render giao dien
              return (  
                <div className="mt-6 p-4 mx-auto h-fit rounded-xl bg-black/40 border border-white/5">
                  <h3 className="text-white/40 text-xs uppercase tracking-widest mb-4">Conclusion: <span className={`${colorClassState}`}>{conclusionState}</span> <span className="italic bg-green-500/20 text-green-300 px-1.5 py-0.5 rounded-md font-extrabold border border-green-500/20">
                      Average Score: {Math.round(avgScore)}/100
                    </span>
                  </h3>
                  <div className={`italic mt-2 p-2 flex text-lg font-medium leading-loose`}>
                    {conclusionText}
                  </div>
                </div>
              );
            })()}

          </div>
        )}

      </div>
    </div>
  );
}

export default App;