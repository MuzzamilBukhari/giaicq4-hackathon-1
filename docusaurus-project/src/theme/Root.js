import React from 'react';
import RAGWidget from '@site/src/components/RAGWidget/RAGWidget';

// Root component wraps the entire application
// This is the perfect place to add global components like the chat widget
export default function Root({ children }) {
  return (
    <>
      {children}
      <RAGWidget endpoint="/api/v1/chat" position="floating" />
    </>
  );
}
