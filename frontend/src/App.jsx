import { useState } from 'react';

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
        sentiment: "Positive",
        score: "95%",
        message: text
      });
      setLoading(false);
    }, 2000);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-teal-950 via-emerald-900 to-green-950 p-8 flex flex-col justify-center relative overflow-hidden">{/* Đổi từ bg-white/10 sang bg-black/40 (Kính râm đen) và giảm viền sáng xuống border-white/10 */}
      <div className="max-w-2xl mx-auto p-10 rounded-2xl bg-white/10 backdrop-blur-xl border border-white/25 shadow-2xl">        {/* Tiêu đề dùng font Serif */}
        <h1 className="text-5xl font-serif text-center mb-8 text-yellow-100 drop-shadow-lg">
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

        {/* Nút bấm thiền tịnh */}
        <button 
          onClick={handleAnalyze} 
          disabled={loading}
          className="w-full mt-6 py-3 rounded-xl bg-green-800/60 hover:bg-green-700/80 text-green-100 font-bold uppercase tracking-widest border border-green-500/30 transition-all active:scale-95 disabled:opacity-50"
        >
          {loading ? "Loading" : "Analyze"}
        </button>

        {/* Khu vực kết quả hiện ra sau khi phân tích */}
        {result && !loading && (
          <div className="mt-8 p-6 rounded-xl bg-white/5 border border-white/10 backdrop-blur-sm">
            <h2 className="text-2xl font-serif text-yellow-100/90 mb-2">Response:</h2>
            <p className="text-green-50 mb-1">State: <strong>{result.sentiment}</strong></p>
            <p className="text-green-50/80 italic">"{result.message}"</p>
          </div>
        )}

      </div>
    </div>
  );
}

export default App;