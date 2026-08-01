import React from 'react';
import { MessageSquare, X } from 'lucide-react';

interface ChatLauncherProps {
  isOpen: boolean;
  onToggle: () => void;
}

export const ChatLauncher: React.FC<ChatLauncherProps> = ({ isOpen, onToggle }) => {
  return (
    <button
      onClick={onToggle}
      className={`fixed bottom-6 right-6 w-14 h-14 rounded-full bg-gradient-to-tr from-indigo-600 to-indigo-500 hover:from-indigo-700 hover:to-indigo-600 text-white shadow-xl shadow-indigo-600/30 flex items-center justify-center transition-all duration-300 hover:scale-105 active:scale-95 z-50 cursor-pointer ${
        isOpen ? 'rotate-90' : ''
      }`}
      aria-label={isOpen ? 'Zamknij czat' : 'Otwórz czat pomocy'}
      title={isOpen ? 'Zamknij czat' : 'Otwórz czat pomocy'}
    >
      {isOpen ? (
        <X className="w-6 h-6" />
      ) : (
        <div className="relative">
          <MessageSquare className="w-6 h-6" />
          <span className="absolute -top-1 -right-1 w-3 h-3 bg-emerald-400 border-2 border-indigo-600 rounded-full animate-pulse"></span>
        </div>
      )}
    </button>
  );
};

export default ChatLauncher;
