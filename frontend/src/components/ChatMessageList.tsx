import React, { useRef, useEffect } from 'react';
import { Message } from '../types/chat';
import ChatMessageItem from './ChatMessageItem';
import ChatTypingIndicator from './ChatTypingIndicator';

interface ChatMessageListProps {
  messages: Message[];
  isLoading: boolean;
}

export const ChatMessageList: React.FC<ChatMessageListProps> = ({ messages, isLoading }) => {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  return (
    <div className="flex-1 bg-slate-50/50 p-4 overflow-y-auto space-y-4">
      {messages.map((msg) => (
        <ChatMessageItem key={msg.id} message={msg} />
      ))}

      {isLoading && <ChatTypingIndicator />}

      <div ref={bottomRef} />
    </div>
  );
};

export default ChatMessageList;
