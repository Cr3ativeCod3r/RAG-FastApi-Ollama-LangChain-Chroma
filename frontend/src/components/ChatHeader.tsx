import React from 'react';
import { Bot, Sparkles, Trash2, X } from 'lucide-react';

interface ChatHeaderProps {
  onClose: () => void;
  onClear: () => void;
}

export const ChatHeader: React.FC<ChatHeaderProps> = ({ onClose, onClear }) => {
  return (
    <div className="bg-gradient-to-r from-indigo-600 via-indigo-600 to-indigo-700 text-white px-5 py-4 flex items-center justify-between shadow-sm select-none">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-white/20 backdrop-blur-md flex items-center justify-center text-white border border-white/25 shadow-inner">
          <Bot className="w-5 h-5 text-white" />
        </div>
        <div>
          <div className="font-semibold text-base tracking-tight flex items-center gap-1.5">
            <span>Doradca AI</span>
            <Sparkles className="w-3.5 h-3.5 text-cyan-300" />
          </div>
          <div className="flex items-center gap-1.5 text-xs text-indigo-100/90 font-medium">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>Online • Baza wiedzy</span>
          </div>
        </div>
      </div>

      <div className="flex items-center gap-1">
        <button
          onClick={onClear}
          className="p-2 rounded-lg text-white/80 hover:text-white hover:bg-white/15 transition-colors cursor-pointer"
          title="Wyczyść rozmowę"
          aria-label="Wyczyść rozmowę"
        >
          <Trash2 className="w-4 h-4" />
        </button>
        <button
          onClick={onClose}
          className="p-2 rounded-lg text-white/80 hover:text-white hover:bg-white/15 transition-colors cursor-pointer"
          title="Zamknij okno czatu"
          aria-label="Zamknij okno czatu"
        >
          <X className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
};

export default ChatHeader;
