export default function PrimaryButton({ children, onClick, disabled }) {
  return (
    <button 
      onClick={onClick} 
      disabled={disabled}
      className="w-full mt-6 py-3 rounded-xl bg-green-800/60 hover:bg-green-700/80 text-green-100 font-bold uppercase tracking-widest border border-green-500/30 transition-all active:scale-95 disabled:opacity-50"
    >
      {children}
    </button>
  );
}
