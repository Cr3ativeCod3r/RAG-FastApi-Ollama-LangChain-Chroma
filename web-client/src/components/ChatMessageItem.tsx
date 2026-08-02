import React from 'react';
import { Bot, User } from 'lucide-react';
import { Message } from '../types/chat';
import ChatSources from './ChatSources';

interface ChatMessageItemProps {
  message: Message;
}

export const ChatMessageItem: React.FC<ChatMessageItemProps> = ({ message }) => {
  const isUser = message.sender === 'user';

  return (
    <div
      className={`flex gap-2.5 max-w-[88%] ${
        isUser ? 'ml-auto flex-row-reverse' : 'mr-auto'
      }`}
    >
      {/* Avatar */}
      <div
        className={`w-7 h-7 rounded-full flex items-center justify-center shrink-0 mt-0.5 text-xs ${
          isUser
            ? 'bg-slate-900 text-white'
            : 'bg-indigo-100 text-indigo-700'
        }`}
      >
        {isUser ? <User className="w-3.5 h-3.5" /> : <Bot className="w-3.5 h-3.5" />}
      </div>

      {/* Message Bubble & Metadata */}
      <div className="space-y-1">
        <div
          className={`px-4 py-3 rounded-2xl text-[13.5px] leading-relaxed shadow-sm ${
            isUser
              ? 'bg-indigo-600 text-white rounded-tr-none shadow-indigo-500/10'
              : 'bg-white text-slate-800 border border-slate-200/80 rounded-tl-none'
          }`}
        >
          <div className="whitespace-pre-wrap">{message.text}</div>

          {/* Sources list */}
          {message.sources && <ChatSources sources={message.sources} />}
        </div>

        <div
          className={`text-[10px] text-slate-400 px-1 ${
            isUser ? 'text-right' : 'text-left'
          }`}
        >
          {message.timestamp}
        </div>
      </div>
    </div>
  );
};

export default ChatMessageItem;
