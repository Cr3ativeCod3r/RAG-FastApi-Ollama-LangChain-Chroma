import React from 'react';
import { useChat } from '../hooks/useChat';
import ChatLauncher from './ChatLauncher';
import ChatModal from './ChatModal';

export const ChatWidget: React.FC = () => {
  const {
    isOpen,
    messages,
    isLoading,
    toggleOpen,
    closeChat,
    clearMessages,
    sendMessage,
  } = useChat();

  return (
    <>
      <ChatModal
        isOpen={isOpen}
        onClose={closeChat}
        onClear={clearMessages}
        messages={messages}
        isLoading={isLoading}
        onSend={sendMessage}
      />
      <ChatLauncher isOpen={isOpen} onToggle={toggleOpen} />
    </>
  );
};

export default ChatWidget;
