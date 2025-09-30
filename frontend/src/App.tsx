import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Layout from './components/Layout/Layout';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Agents from './pages/Agents';
import AgentDetail from './pages/AgentDetail';
import Chat from './pages/Chat';
import AgentForm from './pages/AgentForm';
import Profile from './pages/Profile';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/agents" element={<Agents />} />
            <Route path="/agents/:id" element={<AgentDetail />} />
            <Route path="/chat/:agentId" element={<Chat />} />
            <Route path="/chat/:agentId/:conversationId" element={<Chat />} />
            <Route path="/agents/create" element={<AgentForm />} />
            <Route path="/agents/:id/edit" element={<AgentForm />} />
            <Route path="/profile" element={<Profile />} />
            {/* 更多路由将在后续添加 */}
          </Routes>
        </Layout>
      </Router>
    </AuthProvider>
  );
}

export default App;
