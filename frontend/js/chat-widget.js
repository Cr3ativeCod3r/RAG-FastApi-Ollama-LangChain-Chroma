/**
 * Modular AI Chat Widget Component
 * Communicates with FastAPI RAG backend (/api/v1/ask)
 */
class RagChatWidget {
  constructor(options = {}) {
    this.apiEndpoint = options.apiEndpoint || 'http://localhost:8000/api/v1/ask';
    this.botName = options.botName || 'Asystent AI';
    this.welcomeMessage = options.welcomeMessage || 'Cześć! W czym mogę Ci dzisiaj pomóc?';
    this.isOpen = false;
    this.messages = [];
    this.isGenerating = false;

    this.init();
  }

  init() {
    this.renderWidget();
    this.bindEvents();
    // Add default initial welcome message
    this.addBotMessage(this.welcomeMessage);
  }

  renderWidget() {
    const widgetContainer = document.createElement('div');
    widgetContainer.id = 'rag-chat-widget-root';
    widgetContainer.innerHTML = `
      <!-- Floating Launcher Button -->
      <button class="chat-launcher-btn" id="chatLauncherBtn" aria-label="Otwórz czat pomocy">
        <span class="chat-launcher-status-dot"></span>
        <!-- Chat Icon -->
        <svg class="chat-launcher-icon icon-chat" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
        </svg>
        <!-- Close Icon -->
        <svg class="chat-launcher-icon icon-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>

      <!-- Chat Modal Window -->
      <div class="chat-widget-modal" id="chatWidgetModal" role="dialog" aria-modal="true" aria-hidden="true">
        <!-- Header -->
        <div class="chat-widget-header">
          <div class="chat-header-info">
            <div class="chat-bot-avatar">🤖</div>
            <div>
              <div class="chat-header-title">${this.botName}</div>
              <div class="chat-header-status">
                <span class="chat-status-indicator"></span>
                <span>Dostępny online</span>
              </div>
            </div>
          </div>
          <div class="chat-header-actions">
            <button class="chat-header-btn" id="chatClearBtn" title="Wyczyść rozmowę">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="3 6 5 6 21 6"></polyline>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
              </svg>
            </button>
            <button class="chat-header-btn" id="chatCloseBtn" title="Zamknij okno">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>
        </div>

        <!-- Messages Stream -->
        <div class="chat-widget-body" id="chatWidgetBody">
          <!-- Dynamically populated messages -->
        </div>

        <!-- Footer / Input Form -->
        <div class="chat-widget-footer">
          <form class="chat-input-row" id="chatWidgetForm">
            <input 
              type="text" 
              class="chat-input-field" 
              id="chatInputField" 
              placeholder="Wpisz wiadomość..." 
              autocomplete="off"
              required
            />
            <button type="submit" class="chat-send-btn" id="chatSendBtn" aria-label="Wyślij wiadomość">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
              </svg>
            </button>
          </form>
          <div class="chat-powered-by">
            ⚡ Zasilane przez <b>Ollama RAG</b> & ChromaDB
          </div>
        </div>
      </div>
    `;

    document.body.appendChild(widgetContainer);

    // Cache elements
    this.launcherBtn = document.getElementById('chatLauncherBtn');
    this.modal = document.getElementById('chatWidgetModal');
    this.body = document.getElementById('chatWidgetBody');
    this.form = document.getElementById('chatWidgetForm');
    this.input = document.getElementById('chatInputField');
    this.sendBtn = document.getElementById('chatSendBtn');
    this.closeBtn = document.getElementById('chatCloseBtn');
    this.clearBtn = document.getElementById('chatClearBtn');
  }

  bindEvents() {
    this.launcherBtn.addEventListener('click', () => this.toggle());
    this.closeBtn.addEventListener('click', () => this.close());
    this.clearBtn.addEventListener('click', () => this.clearHistory());

    this.form.addEventListener('submit', (e) => {
      e.preventDefault();
      this.handleUserSubmit();
    });

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && this.isOpen) {
        this.close();
      }
    });
  }

  toggle() {
    if (this.isOpen) {
      this.close();
    } else {
      this.open();
    }
  }

  open() {
    this.isOpen = true;
    this.launcherBtn.classList.add('is-active');
    this.modal.classList.add('is-open');
    this.modal.setAttribute('aria-hidden', 'false');
    setTimeout(() => this.input.focus(), 150);
    this.scrollToBottom();
  }

  close() {
    this.isOpen = false;
    this.launcherBtn.classList.remove('is-active');
    this.modal.classList.remove('is-open');
    this.modal.setAttribute('aria-hidden', 'true');
  }

  clearHistory() {
    this.body.innerHTML = '';
    this.messages = [];
    this.addBotMessage(this.welcomeMessage);
  }

  addUserMessage(text) {
    const row = document.createElement('div');
    row.className = 'chat-msg-row user';
    row.innerHTML = `
      <div class="chat-msg-avatar">👤</div>
      <div class="chat-msg-bubble">${this.escapeHtml(text)}</div>
    `;
    this.body.appendChild(row);
    this.scrollToBottom();
  }

  addBotMessage(text, sources = []) {
    const row = document.createElement('div');
    row.className = 'chat-msg-row bot';

    let sourcesMarkup = '';
    if (sources && sources.length > 0) {
      const badges = sources.map(s => {
        const meta = s.metadata || {};
        const nr = meta.nr_pytania || meta.id || meta.row_index || '?';
        const sheet = meta.sheet_name || 'FAQ';
        return `<span class="chat-source-badge">Arkusz: ${sheet} | Nr: ${nr}</span>`;
      }).join('');

      sourcesMarkup = `
        <div class="chat-sources-panel">
          <div class="chat-sources-label">📚 Źródła z Excela:</div>
          <div>${badges}</div>
        </div>
      `;
    }

    const formattedText = text.replace(/\n/g, '<br>');

    row.innerHTML = `
      <div class="chat-msg-avatar">🤖</div>
      <div class="chat-msg-bubble">
        <div>${formattedText}</div>
        ${sourcesMarkup}
      </div>
    `;

    this.body.appendChild(row);
    this.scrollToBottom();
    return row;
  }

  showTypingIndicator() {
    const row = document.createElement('div');
    row.className = 'chat-msg-row bot';
    row.id = 'chatTypingIndicator';
    row.innerHTML = `
      <div class="chat-msg-avatar">🤖</div>
      <div class="chat-typing-bubble">
        <span class="chat-typing-dot"></span>
        <span class="chat-typing-dot"></span>
        <span class="chat-typing-dot"></span>
      </div>
    `;
    this.body.appendChild(row);
    this.scrollToBottom();
  }

  hideTypingIndicator() {
    const indicator = document.getElementById('chatTypingIndicator');
    if (indicator) {
      indicator.remove();
    }
  }

  scrollToBottom() {
    this.body.scrollTop = this.body.scrollHeight;
  }

  escapeHtml(unsafe) {
    return unsafe
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  async handleUserSubmit() {
    const query = this.input.value.trim();
    if (!query || this.isGenerating) return;

    this.addUserMessage(query);
    this.input.value = '';
    this.isGenerating = true;
    this.sendBtn.disabled = true;

    this.showTypingIndicator();

    try {
      const response = await fetch(this.apiEndpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: query })
      });

      this.hideTypingIndicator();

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Błąd serwera (${response.status})`);
      }

      const data = await response.json();
      this.addBotMessage(data.answer, data.sources);
    } catch (err) {
      this.hideTypingIndicator();
      this.addBotMessage(`Przepraszam, wystąpił problem z połączeniem (${err.message}). Upewnij się, że backend RAG jest włączony na porcie 8000.`);
    } finally {
      this.isGenerating = false;
      this.sendBtn.disabled = false;
      this.input.focus();
    }
  }
}

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  window.ragChatWidget = new RagChatWidget({
    apiEndpoint: 'http://localhost:8000/api/v1/ask',
    botName: 'Doradca Klienta AI',
    welcomeMessage: 'Cześć! W czym mogę Ci dzisiaj pomóc?'
  });
});
