import React, { useState, useRef, useEffect } from 'react';
import './rag-widget.css';

const RAGWidget = ({ endpoint = 'http://localhost:8000/api/ask', position = 'floating' }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { id: 1, text: 'Hello! I\'m your book assistant. Ask me anything about the content in this book, and I\'ll find the relevant information for you.', sender: 'assistant' }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [selectedText, setSelectedText] = useState('');

  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const containerRef = useRef(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Set up text selection listener
  useEffect(() => {
    const handleTextSelection = () => {
      const selection = window.getSelection();
      if (selection && selection.toString().trim() && selection.toString().trim().length > 10) {
        const selectedText = selection.toString().trim();
        setSelectedText(selectedText.substring(0, 200) + (selectedText.length > 200 ? '...' : ''));
      }
    };

    document.addEventListener('mouseup', handleTextSelection);
    return () => {
      document.removeEventListener('mouseup', handleTextSelection);
    };
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const generateSessionId = () => {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
  };

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = { id: Date.now(), text: inputValue, sender: 'user' };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setError(null);

    try {
      // Generate session ID if we don't have one
      const currentSessionId = sessionId || generateSessionId();
      if (!sessionId) {
        setSessionId(currentSessionId);
      }

      // Prepare request body
      const requestBody = {
        question: inputValue.trim(),
        session_id: currentSessionId
      };

      // Make API request
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify(requestBody)
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(`API request failed: ${response.status} ${response.statusText}. ${errorData.detail || ''}`);
      }

      const responseData = await response.json();

      // Add assistant response to messages
      const assistantMessage = {
        id: Date.now() + 1,
        text: responseData.answer || 'I received your message but there was an issue with the response.',
        sender: 'assistant'
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (err) {
      console.error('Error sending message:', err);
      setError(err.message);

      // Add error message to chat
      const errorMessage = {
        id: Date.now() + 1,
        text: `Sorry, I encountered an error: ${err.message}. Please try again.`,
        sender: 'system'
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      setSelectedText('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const toggleWidget = () => {
    setIsOpen(!isOpen);
  };

  const clearContext = () => {
    setSelectedText('');
  };

  return (
    <div className={`rag-widget ${position} ${isOpen ? 'open' : 'closed'}`} ref={containerRef}>
      {!isOpen ? (
        <button className="rag-widget-toggle" onClick={toggleWidget}>
          💬
        </button>
      ) : (
        <div className="rag-widget-container">
          <div className="rag-widget-header">
            <h3>Book Assistant</h3>
            <button className="rag-widget-close" onClick={toggleWidget}>
              ×
            </button>
          </div>

          <div className="rag-widget-messages">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`rag-widget-message ${message.sender}`}
              >
                <div className="rag-widget-message-text">
                  {message.text}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="rag-widget-message assistant">
                <div className="rag-widget-message-text">
                  <div className="rag-widget-typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            {error && (
              <div className="rag-widget-message system">
                <div className="rag-widget-message-text error">
                  Error: {error}
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {selectedText && (
            <div className="rag-widget-context">
              <div className="rag-widget-context-header">Selected Text Context:</div>
              <div className="rag-widget-context-content">{selectedText}</div>
              <button className="rag-widget-clear-context" onClick={clearContext}>
                Clear Context
              </button>
            </div>
          )}

          <div className="rag-widget-input-area">
            <textarea
              ref={inputRef}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask a question about this book..."
              rows="3"
              className="rag-widget-input"
              disabled={isLoading}
            />
            <button
              onClick={sendMessage}
              className="rag-widget-send-btn"
              disabled={isLoading || !inputValue.trim()}
            >
              {isLoading ? 'Sending...' : 'Send'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default RAGWidget;