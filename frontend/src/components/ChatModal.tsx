import React, { useEffect } from 'react';
import { Message } from '../types/chat';
import ChatHeader from './ChatHeader';
import ChatMessageList from './ChatMessageList';
import ChatInput from './ChatInput';

interface ChatModalProps {
  isOpen: boolean;
  onClose: () => void;
  onClear: () => void;
  messages: Message[];
  isLoading: boolean;
  onSend: (text: string) => void;
}

export const ChatModal: React.FC<ChatModalProps> = ({
  isOpen,
  onClose,
  onClear,
  messages,
  isLoading,
  onSend,
}) => {
  // Close on Escape key press
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div
      className="fixed bottom-24 right-6 w-[410px] max-w-[calc(100vw-32px)] h-[600px] max-h-[calc(100vh-120px)] bg-white rounded-3xl shadow-2xl shadow-slate-900/15 border border-slate-200/90 flex flex-col overflow-hidden z-50 animate-in fade-in zoom-in-95 duration-200 origin-bottom-right"
      role="dialog"
      aria-modal="true"
      aria-label="Okno czatu pomocy"
    >
      <ChatHeader onClose={onClose} onClear={onClear} />
      <ChatMessageList messages={messages} isLoading={isLoading} />
      <ChatInput onSend={onSend} disabled={isLoading} />
    </div>
  );
};

export default ChatModal;
