import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import RAGChatWidget from '@site/src/components/RAGChatWidget';

// Default backend URL - can be overridden by environment or build process
const BACKEND_URL = process.env.RAG_BACKEND_URL || 'https://your-rag-backend.railway.app';
const ALLOWED_ORIGINS = process.env.ALLOWED_ORIGINS?.split(',') || ['https://yourdomain.com'];

export default function LayoutWrapper(props) {
  return (
    <>
      <OriginalLayout {...props}>
        {props.children}
        <RAGChatWidget
          backendUrl={BACKEND_URL}
          allowedOrigins={ALLOWED_ORIGINS}
        />
      </OriginalLayout>
    </>
  );
}