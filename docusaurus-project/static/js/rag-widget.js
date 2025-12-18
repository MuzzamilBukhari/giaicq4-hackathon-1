/**
 * RAG Agent Widget for Docusaurus Integration
 * Provides an interactive chat interface that connects to the RAG Agent API
 */
class RAGWidget {
  constructor(options = {}) {
    this.endpoint = options.endpoint || '/api/v1/chat';  // Updated to match backend API
    this.containerId = options.containerId || 'rag-agent-widget';
    this.container = null;
    this.sessionId = options.sessionId || null;
    this.onResponse = options.onResponse || null;
    this.onError = options.onError || null;

    this.initializeWidget();
  }

  initializeWidget() {
    // Get the container element
    this.container = document.getElementById(this.containerId);
    if (!this.container) {
      console.error(`Container with id '${this.containerId}' not found`);
      return;
    }

    // Create the widget HTML structure
    this.container.innerHTML = `
      <div id="rag-agent-interface" class="rag-agent-container">
        <div id="rag-agent-header" class="rag-agent-header">
          <h3>Book Assistant</h3>
          <div id="rag-agent-status" class="rag-agent-status">Ready</div>
        </div>

        <div id="rag-agent-messages" class="rag-agent-messages">
          <div class="rag-agent-message rag-agent-welcome">
            <p>Hello! I'm your book assistant. Ask me anything about the content in this book, and I'll find the relevant information for you.</p>
          </div>
        </div>

        <div id="rag-agent-input-area" class="rag-agent-input-area">
          <textarea
            id="rag-agent-input"
            class="rag-agent-input"
            placeholder="Ask a question about this book..."
            rows="3"
          ></textarea>
          <button id="rag-agent-send" class="rag-agent-send-btn">Send</button>
        </div>

        <div id="rag-agent-selected-text" class="rag-agent-selected-text" style="display: none;">
          <div class="rag-agent-context-header">Selected Text Context:</div>
          <div id="rag-agent-context-content" class="rag-agent-context-content"></div>
          <button id="rag-agent-clear-context" class="rag-agent-clear-btn">Clear Context</button>
        </div>
      </div>
    `;

    // Bind events
    this.bindEvents();

    // Check if we have selected text functionality
    this.setupTextSelection();
  }

  bindEvents() {
    const input = document.getElementById('rag-agent-input');
    const sendBtn = document.getElementById('rag-agent-send');
    const clearContextBtn = document.getElementById('rag-agent-clear-context');

    // Send message on button click
    sendBtn.addEventListener('click', () => this.sendMessage());

    // Send message on Enter (without Shift)
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        this.sendMessage();
      }
    });

    // Clear context
    if (clearContextBtn) {
      clearContextBtn.addEventListener('click', () => this.clearContext());
    }
  }

  setupTextSelection() {
    // Add text selection event listeners to capture selected text
    document.addEventListener('mouseup', () => {
      setTimeout(() => {
        const selectedText = this.getSelectedText();
        if (selectedText && selectedText.length > 10) { // Only if meaningful text is selected
          this.showContext(selectedText);
        }
      }, 0);
    });
  }

  getSelectedText() {
    const selection = window.getSelection();
    if (selection && selection.toString().trim()) {
      return selection.toString().trim();
    }
    return '';
  }

  showContext(text) {
    const contextContainer = document.getElementById('rag-agent-selected-text');
    const contextContent = document.getElementById('rag-agent-context-content');

    if (contextContainer && contextContent) {
      contextContent.textContent = text.substring(0, 200) + (text.length > 200 ? '...' : '');
      contextContainer.style.display = 'block';
      this.currentContext = text;
    }
  }

  clearContext() {
    const contextContainer = document.getElementById('rag-agent-selected-text');
    if (contextContainer) {
      contextContainer.style.display = 'none';
      this.currentContext = null;
    }
  }

  async sendMessage() {
    const input = document.getElementById('rag-agent-input');
    const message = input.value.trim();

    if (!message) return;

    // Add user message to chat
    this.addMessage(message, 'user');

    // Clear input
    input.value = '';

    // Update status
    this.updateStatus('Thinking...');

    try {
      // Prepare the request - Updated to match backend API
      const requestBody = {
        query: message,  // Changed from 'message' to 'query'
        session_id: this.sessionId || null,
        metadata: this.currentContext ? { context: this.currentContext } : null  // Added context as metadata
      };

      // Make the request to the API
      const response = await fetch(this.endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody)
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status} ${response.statusText}`);
      }

      // Handle the response (non-streaming for now)
      const responseData = await response.json();

      // Add the response to the chat
      this.addMessage(responseData.answer, 'assistant');

      // Add sources if available
      if (responseData.sources && responseData.sources.length > 0) {
        this.addSources(responseData.sources);
      }

      // Update status
      this.updateStatus('Ready');

      // Generate new session ID if we didn't have one
      if (!this.sessionId) {
        this.sessionId = this.generateSessionId();
      }

      // Call response callback if provided
      if (this.onResponse) {
        this.onResponse(responseData.answer, responseData.sources);
      }

    } catch (error) {
      console.error('Error sending message:', error);
      this.addMessage('Sorry, I encountered an error processing your request.', 'system');
      this.updateStatus('Error - click to retry');

      if (this.onError) {
        this.onError(error);
      }
    }
  }

  addMessage(text, sender) {
    const messagesContainer = document.getElementById('rag-agent-messages');
    if (!messagesContainer) return;

    const messageDiv = document.createElement('div');
    messageDiv.className = `rag-agent-message rag-agent-${sender}`;

    // Sanitize the text to prevent XSS
    const sanitizedText = this.sanitizeHTML(text);

    messageDiv.innerHTML = `<p>${sanitizedText}</p>`;
    messagesContainer.appendChild(messageDiv);

    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  updateLastAssistantMessage(text) {
    const messagesContainer = document.getElementById('rag-agent-messages');
    if (!messagesContainer) return;

    const messages = messagesContainer.querySelectorAll('.rag-agent-message');
    if (messages.length === 0) return;

    let lastAssistantMsg = null;
    // Find the last assistant message
    for (let i = messages.length - 1; i >= 0; i--) {
      if (messages[i].classList.contains('rag-agent-assistant')) {
        lastAssistantMsg = messages[i];
        break;
      }
    }

    if (lastAssistantMsg) {
      // Update the content
      lastAssistantMsg.innerHTML = `<p>${this.sanitizeHTML(text)}</p>`;
    } else {
      // Create a new assistant message
      this.addMessage(text, 'assistant');
    }

    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  addSources(sources) {
    if (sources.length === 0) return;

    const messagesContainer = document.getElementById('rag-agent-messages');
    if (!messagesContainer) return;

    const sourcesDiv = document.createElement('div');
    sourcesDiv.className = 'rag-agent-sources';

    sourcesDiv.innerHTML = `
      <div class="rag-agent-sources-header">Sources:</div>
      <ul class="rag-agent-sources-list">
        ${sources.map(source => `
          <li>
            <a href="${this.sanitizeHTML(source.url)}" target="_blank" rel="noopener noreferrer">
              ${this.sanitizeHTML(source.section || 'Unknown Section')}
            </a>
            ${source.relevance_score ? ` (Relevance: ${(source.relevance_score * 100).toFixed(0)}%)` : ''}
          </li>
        `).join('')}
      </ul>
    `;

    messagesContainer.appendChild(sourcesDiv);

    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  updateStatus(status) {
    const statusElement = document.getElementById('rag-agent-status');
    if (statusElement) {
      statusElement.textContent = status;
    }
  }

  sanitizeHTML(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  generateSessionId() {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
  }

  // Static method to initialize the widget
  static init(options) {
    return new RAGWidget(options);
  }
}

// Auto-initialize if the container exists on page load
document.addEventListener('DOMContentLoaded', function() {
  const defaultContainer = document.getElementById('rag-agent-widget');
  if (defaultContainer) {
    window.RAGWidget = RAGWidget;
    // Don't auto-initialize, let the user decide when to call RAGWidget.init()
  }
});

// Make RAGWidget globally available
if (typeof window !== 'undefined') {
  window.RAGWidget = RAGWidget;
}