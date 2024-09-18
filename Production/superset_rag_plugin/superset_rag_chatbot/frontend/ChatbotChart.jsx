import React, { useState } from 'react';
import { Input, Button, Typography } from 'antd';

const { Text } = Typography;

export default function ChatbotChart() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const res = await fetch('/rag-chatbot/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });
      const data = await res.json();
      setResponse(data.response);
    } catch (error) {
      setResponse('Error: Unable to get response from chatbot.');
      console.error('Chatbot error:', error);
    }
    setLoading(false);
  };

  return (
    <div className="chatbot-container">
      <Input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask a question..."
        onPressEnter={handleSubmit}
      />
      <Button onClick={handleSubmit} disabled={loading}>
        {loading ? 'Loading...' : 'Send'}
      </Button>
      {response && (
        <div className="response-container">
          <Text strong>Response:</Text>
          <Text>{response}</Text>
        </div>
      )}
    </div>
  );
}