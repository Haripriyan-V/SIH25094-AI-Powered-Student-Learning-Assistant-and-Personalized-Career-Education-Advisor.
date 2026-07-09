import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { PaperAirplaneIcon, ChatBubbleBottomCenterTextIcon } from '@heroicons/react/24/outline';
import api from '../../services/api';
import { Loader } from '../../components/common/Loader';

function ChatMessage({ msg }) {
  const isUser = msg.sender === 'user';
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}
    >
      <div
        className={`max-w-xs lg:max-w-md px-4 py-3 rounded-2xl ${
          isUser
            ? 'bg-iris-500 text-white rounded-br-none'
            : 'surface text-ink-900 dark:text-ink-50 rounded-bl-none'
        }`}
      >
        <p className="text-sm leading-relaxed">{msg.message}</p>
        <p className={`text-xs mt-1 ${isUser ? 'text-iris-100' : 'text-ink-400 dark:text-ink-500'}`}>
          {new Date(msg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </p>
      </div>
    </motion.div>
  );
}

export default function Chat() {
  const [sessions, setSessions] = useState([]);
  const [activeSession, setActiveSession] = useState(null);
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);

  // Load sessions on mount
  useEffect(() => {
    api
      .get('/chatbot/sessions/')
      .then((res) => {
        const sessionsData = res.data;
        const list = Array.isArray(sessionsData) ? sessionsData : sessionsData.results || [];
        setSessions(list);
        if (list.length > 0) {
          setActiveSession(list[0]);
          setMessages(list[0].messages || []);
        }
      })
      .catch((err) => console.error('Error loading chat sessions:', err))
      .finally(() => setLoading(false));
  }, []);

  const handleNewSession = () => {
    api
      .post('/chatbot/sessions/', { title: `Chat ${new Date().toLocaleDateString()}` })
      .then((res) => {
        setSessions([res.data, ...sessions]);
        setActiveSession(res.data);
        setMessages([]);
      })
      .catch((err) => console.error('Error creating chat session:', err));
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputText.trim() || !activeSession || sending) return;

    setSending(true);
    try {
      const res = await api.post(`/chatbot/sessions/${activeSession.id}/send_message/`, {
        message: inputText,
      });
      setMessages([
        ...messages,
        res.data.user_message,
        res.data.assistant_message,
      ]);
      setInputText('');
    } catch (err) {
      console.error('Error sending message:', err);
    } finally {
      setSending(false);
    }
  };

  if (loading) return <Loader label="Loading chat…" size="lg" />;

  return (
    <div className="flex h-[calc(100vh-8rem)] gap-4">
      {/* Sidebar - Sessions list */}
      <div className="w-64 hidden lg:flex flex-col border-r border-ink-100 dark:border-ink-800 bg-ink-25 dark:bg-ink-950 rounded-2xl p-4">
        <button
          onClick={handleNewSession}
          className="btn-primary w-full mb-4"
        >
          + New Chat
        </button>
        <div className="flex-1 overflow-y-auto space-y-2">
          {sessions.map((session) => (
            <button
              key={session.id}
              onClick={() => {
                setActiveSession(session);
                setMessages(session.messages || []);
              }}
              className={`w-full text-left px-3 py-2 rounded-xl transition-colors text-sm font-medium truncate ${
                activeSession?.id === session.id
                  ? 'bg-iris-500 text-white'
                  : 'text-ink-700 dark:text-ink-300 hover:bg-ink-200 dark:hover:bg-ink-800'
              }`}
            >
              {session.title || `Session #${session.id}`}
            </button>
          ))}
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {activeSession ? (
          <>
            {/* Header */}
            <div className="mb-4">
              <h1 className="text-2xl font-semibold text-ink-900 dark:text-ink-50">
                {activeSession.title || 'Chat with AI'}
              </h1>
              <p className="text-sm text-ink-500 dark:text-ink-400">
                AI Learning Assistant
              </p>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto mb-4 p-4 bg-ink-50 dark:bg-ink-900/50 rounded-2xl">
              {messages.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-full text-center">
                  <ChatBubbleBottomCenterTextIcon className="h-12 w-12 text-ink-300 dark:text-ink-600 mb-3" />
                  <p className="text-ink-500 dark:text-ink-400">Start a conversation with the AI assistant</p>
                </div>
              ) : (
                messages.map((msg) => (
                  <ChatMessage key={msg.id} msg={msg} />
                ))
              )}
            </div>

            {/* Input */}
            <form onSubmit={handleSendMessage} className="flex gap-3">
              <input
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder="Type your message…"
                disabled={sending}
                className="flex-1 input"
              />
              <button
                type="submit"
                disabled={sending || !inputText.trim()}
                className="btn-primary"
              >
                <PaperAirplaneIcon className="h-4 w-4" />
              </button>
            </form>
          </>
        ) : (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <ChatBubbleBottomCenterTextIcon className="h-12 w-12 text-ink-300 dark:text-ink-600 mb-3" />
            <p className="text-ink-500 dark:text-ink-400 mb-6">No chat sessions yet</p>
            <button onClick={handleNewSession} className="btn-primary">
              Create a new chat
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
