import React, { useEffect, useRef, useState } from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './rag-widget.module.css';

// RAG Widget Component for Docusaurus
const RAGWidget = ({ endpoint = '/api/v1/chat', position = 'floating' }) => {
  const { siteConfig } = useDocusaurusContext();
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [isOpen, setIsOpen] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Initialize session ID
  useEffect(() => {
    if (!sessionId) {
      setSessionId('session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9));
    }
  }, [sessionId]);

  // Handle sending a message
  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: inputValue.trim(),
      timestamp: new Date()
    };

    // Add user message to chat
    setMessages(prev => [...prev, userMessage]);
    const newInputValue = inputValue.trim();
    setInputValue('');
    setIsLoading(true);

    try {
      // Get selected text context if any
      const selectedText = window.getSelection?.()?.toString()?.trim() || '';

      // Prepare the request - Updated to match backend API
      const requestBody = {
        query: newInputValue,  // Changed from 'message' to 'query'
        session_id: sessionId,
        metadata: selectedText ? { context: selectedText } : null  // Added context as metadata
      };

      // Make the API call
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody)
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status}`);
      }

      // Handle JSON response from backend
      const responseData = await response.json();

      // Create assistant message with response data
      const assistantMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: responseData.answer,
        sources: responseData.sources || [],
        timestamp: new Date()
      };

      // Add the response to the messages
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, {
        id: Date.now() + Math.random(),
        role: 'error',
        content: 'Sorry, there was an error processing your request. Please try again.',
        timestamp: new Date()
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle key press (Enter to send)
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  // Toggle widget open/close
  const toggleWidget = () => {
    setIsOpen(!isOpen);
  };

  // For floating position, render the button and popup
  if (position === 'floating') {
    return (
      <>
        {/* Floating Chat Button */}
        <button
          className={styles.floatingChatButton}
          onClick={toggleWidget}
          aria-label="Open chat assistant"
        >
          {isOpen ? '✕' : '💬'}
        </button>

        {/* Chat Popup */}
        {isOpen && (
          <div className={styles.chatPopup}>
            <div className={styles.ragWidgetContainer}>
              <div className={styles.ragWidgetHeader}>
                <h3>📚 Book Assistant</h3>
                <button 
                  className={styles.closeButton}
                  onClick={toggleWidget}
                  aria-label="Close chat"
                >
                  ✕
                </button>
              </div>
              <div className={styles.ragWidgetChat}>
                <div className={styles.ragWidgetMessages}>
                  {messages.length === 0 ? (
                    <div className={styles.ragWidgetWelcome}>
                      Ask me anything about the Physical AI & Humanoid Robotics textbook!
                    </div>
                  ) : (
                    messages.map((message) => (
                      <div
                        key={message.id}
                        className={`${styles.ragWidgetMessage} ${styles[`ragWidgetMessage${message.role.charAt(0).toUpperCase() + message.role.slice(1)}`]}`}
                      >
                        {message.role === 'user' || message.role === 'assistant' ? (
                          <>
                            <div className={styles.ragWidgetMessageContent}>
                              {message.content}
                            </div>
                            <div className={styles.ragWidgetMessageRole}>
                              {message.role === 'user' ? 'You' : 'Assistant'}
                            </div>
                          </>
                        ) : message.role === 'warning' ? (
                          <div className={styles.ragWidgetMessageContent}>
                            {message.content}
                          </div>
                        ) : message.role === 'error' ? (
                          <div className={styles.ragWidgetMessageContent}>
                            {message.content}
                          </div>
                        ) : null}

                        {message.sources && message.sources.length > 0 && (
                          <div className={styles.ragWidgetSources}>
                            <div className={styles.ragWidgetSourcesHeader}>Sources:</div>
                            <ul className={styles.ragWidgetSourcesList}>
                              {message.sources.map((source, index) => (
                                <li key={index}>
                                  <a
                                    href={source.url || '#'}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                  >
                                    {source.section || source.url || 'Unknown source'}
                                  </a>
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    ))
                  )}
                  <div ref={messagesEndRef} />
                </div>
                <div className={styles.ragWidgetInputContainer}>
                  <textarea
                    ref={inputRef}
                    className={styles.ragWidgetInput}
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Ask a question about the book content..."
                    rows="3"
                    disabled={isLoading}
                  />
                  <button
                    className={styles.ragWidgetSendBtn}
                    onClick={sendMessage}
                    disabled={isLoading || !inputValue.trim()}
                  >
                    {isLoading ? 'Sending...' : 'Send'}
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </>
    );
  }

  // For inline/sidebar position, render normally
  return (
    <div className={styles.ragWidgetContainer}>
      <div className={styles.ragWidgetHeader}>
        <h3>📚 Book Assistant</h3>
        <div className={styles.ragWidgetStatus}>
          {isLoading ? 'Thinking...' : 'Ready'}
        </div>
      </div>
      <div className={styles.ragWidgetChat}>
        <div className={styles.ragWidgetMessages}>
          {messages.length === 0 ? (
            <div className={styles.ragWidgetWelcome}>
              Ask me anything about the Physical AI & Humanoid Robotics textbook!
            </div>
          ) : (
            messages.map((message) => (
              <div
                key={message.id}
                className={`${styles.ragWidgetMessage} ${styles[`ragWidgetMessage${message.role.charAt(0).toUpperCase() + message.role.slice(1)}`]}`}
              >
                {message.role === 'user' || message.role === 'assistant' ? (
                  <>
                    <div className={styles.ragWidgetMessageContent}>
                      {message.content}
                    </div>
                    <div className={styles.ragWidgetMessageRole}>
                      {message.role === 'user' ? 'You' : 'Assistant'}
                    </div>
                  </>
                ) : message.role === 'warning' ? (
                  <div className={styles.ragWidgetMessageContent}>
                    {message.content}
                  </div>
                ) : message.role === 'error' ? (
                  <div className={styles.ragWidgetMessageContent}>
                    {message.content}
                  </div>
                ) : null}

                {message.sources && message.sources.length > 0 && (
                  <div className={styles.ragWidgetSources}>
                    <div className={styles.ragWidgetSourcesHeader}>Sources:</div>
                    <ul className={styles.ragWidgetSourcesList}>
                      {message.sources.map((source, index) => (
                        <li key={index}>
                          <a
                            href={source.url || '#'}
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            {source.section || source.url || 'Unknown source'}
                          </a>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))
          )}
          <div ref={messagesEndRef} />
        </div>
        <div className={styles.ragWidgetInputContainer}>
          <textarea
            ref={inputRef}
            className={styles.ragWidgetInput}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask a question about the book content..."
            rows="3"
            disabled={isLoading}
          />
          <button
            className={styles.ragWidgetSendBtn}
            onClick={sendMessage}
            disabled={isLoading || !inputValue.trim()}
          >
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default RAGWidget;
