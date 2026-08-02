import React from 'react';
import ChatWidget from './components/ChatWidget';

const App: React.FC = () => {
  return (
    <main className="min-h-screen w-full bg-white relative">
      {/* Pure white page - Chat widget anchored to bottom-right corner */}
      <ChatWidget />
    </main>
  );
};

export default App;
