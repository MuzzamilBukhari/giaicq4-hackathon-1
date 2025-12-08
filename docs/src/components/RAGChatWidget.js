import React, { useState, useEffect } from 'react';
import { useColorMode } from '@docusaurus/theme-common';
import './RAGChatWidget.css';

const RAGChatWidget = ({ backendUrl = 'http://localhost:8000', allowedOrigins = [] }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const [useSelectedText, setUseSelectedText] = useState(false);
  const [error, setError] = useState('');

  const { colorMode } = useColorMode();

  // Check for selected text
  useEffect(() => {
    const handleSelection = () => {
      const text = window.getSelection().toString().trim();
      if (text.length > 0 && text.length < 1000) { // Only capture reasonable selections
        setSelectedText(text);
      }
    };

    document.addEventListener('mouseup', handleSelection);
    return () => document.removeEventListener('mouseup', handleSelection);
  }, []);

  const toggleWidget = () => {
    setIsOpen(!isOpen);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMessage = { role: 'user', content: inputValue };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError('');

    try {
      let response;
      if (useSelectedText && selectedText) {
        // Use selected text only mode
        response = await fetch(`${backendUrl}/selected`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            question: inputValue,
            selected_text: selectedText,
          }),
        });
      } else {
        // Full retrieval mode
        response = await fetch(`${backendUrl}/query`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            question: inputValue,
            mode: 'full_retrieval',
          }),
        });
      }

      if (!response.ok) {
        throw new Error(`API error: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();

      const botMessage = {
        role: 'assistant',
        content: data.answer,
        sources: data.sources || [],
      };

      setMessages(prev => [...prev, botMessage]);
      setInputValue('');
    } catch (err) {
      setError(`Error: ${err.message}`);
      console.error('Chat error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([]);
    setError('');
  };

  return (
    <>
      {/* Chat Widget Button */}
      <button
        className={`rag-chat-button ${colorMode}`}
        onClick={toggleWidget}
        aria-label="Open RAG Chat"
      >
        💬 AI Assistant
      </button>

      {/* Chat Widget Modal */}
      {isOpen && (
        <div className={`rag-chat-modal ${colorMode}`}>
          <div className="rag-chat-header">
            <h3>Textbook AI Assistant</h3>
            <div className="rag-chat-controls">
              <button onClick={clearChat} className="rag-clear-button" title="Clear chat">
                🗑️
              </button>
              <button onClick={toggleWidget} className="rag-close-button" title="Close">
                ✕
              </button>
            </div>
          </div>

          <div className="rag-chat-body">
            {messages.length === 0 ? (
              <div className="rag-welcome-message">
                <p>Ask me anything about this textbook! I can help explain concepts and find relevant information.</p>
                {selectedText && (
                  <div className="rag-selected-text-notice">
                    <p>Detected selected text: "{selectedText.substring(0, 50)}..."</p>
                    <label>
                      <input
                        type="checkbox"
                        checked={useSelectedText}
                        onChange={(e) => setUseSelectedText(e.target.checked)}
                      />
                      Use selected text only
                    </label>
                  </div>
                )}
              </div>
            ) : (
              <div className="rag-messages">
                {messages.map((msg, index) => (
                  <div key={index} className={`rag-message ${msg.role}`}>
                    <div className="rag-message-content">
                      {msg.content}
                    </div>
                    {msg.sources && msg.sources.length > 0 && (
                      <div className="rag-sources">
                        <details>
                          <summary>Sources ({msg.sources.length})</summary>
                          <ul>
                            {msg.sources.map((source, srcIndex) => (
                              <li key={srcIndex}>
                                <a
                                  href={source.doc_path.replace('/docs', '')}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                >
                                  {source.heading || source.doc_path}
                                </a>
                                <p className="rag-source-excerpt">{source.excerpt}</p>
                              </li>
                            ))}
                          </ul>
                        </details>
                      </div>
                    )}
                  </div>
                ))}
                {isLoading && (
                  <div className="rag-message assistant">
                    <div className="rag-typing-indicator">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                )}
              </div>
            )}

            {error && (
              <div className="rag-error">
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit} className="rag-input-form">
              {selectedText && (
                <div className="rag-selected-text-preview">
                  <small>Using selected text: "{selectedText.substring(0, 30)}..."</small>
                </div>
              )}
              <div className="rag-input-controls">
                <input
                  type="text"
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  placeholder="Ask a question about the textbook..."
                  disabled={isLoading}
                  className="rag-input"
                />
                <button type="submit" disabled={isLoading || !inputValue.trim()}>
                  {isLoading ? 'Sending...' : 'Send'}
                </button>
              </div>
              {selectedText && (
                <label className="rag-checkbox-label">
                  <input
                    type="checkbox"
                    checked={useSelectedText}
                    onChange={(e) => setUseSelectedText(e.target.checked)}
                  />
                  Use selected text only
                </label>
              )}
            </form>
          </div>
        </div>
      )}
    </>
  );
};

export default RAGChatWidget;