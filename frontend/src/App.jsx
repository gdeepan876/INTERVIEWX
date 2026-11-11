import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import HomePage from './pages/HomePage';
import SetupPage from './pages/SetupPage';
import InterviewRoomPage from './pages/InterviewRoomPage';
import ReportPage from './pages/ReportPage';
import HistoryPage from './pages/HistoryPage';

export default function App() {
  const [currentRoute, setCurrentRoute] = useState('home');
  const [activeSession, setActiveSession] = useState(null);
  const [reportInterviewId, setReportInterviewId] = useState(null);

  const handleNavigate = (route) => {
    setCurrentRoute(route);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleStartInterview = () => {
    handleNavigate('setup');
  };

  const handleSessionStarted = (sessionData) => {
    setActiveSession(sessionData);
    handleNavigate('room');
  };

  const handleInterviewComplete = (interviewId) => {
    setReportInterviewId(interviewId);
    handleNavigate('report');
  };

  const handleSelectHistorySession = (interviewId) => {
    setReportInterviewId(interviewId);
    handleNavigate('report');
  };

  const handleExitRoom = () => {
    setActiveSession(null);
    handleNavigate('home');
  };

  return (
    <div className="app-container">
      <Navbar currentRoute={currentRoute} onNavigate={handleNavigate} />

      <main className="main-content">
        {currentRoute === 'home' && (
          <HomePage 
            onStartInterview={handleStartInterview} 
            onNavigate={handleNavigate} 
          />
        )}

        {currentRoute === 'setup' && (
          <SetupPage 
            onSessionStarted={handleSessionStarted} 
          />
        )}

        {currentRoute === 'room' && activeSession && (
          <InterviewRoomPage
            sessionData={activeSession}
            onInterviewComplete={handleInterviewComplete}
            onExit={handleExitRoom}
          />
        )}

        {currentRoute === 'report' && (
          <ReportPage
            interviewId={reportInterviewId}
            onNewInterview={handleStartInterview}
            onNavigate={handleNavigate}
          />
        )}

        {currentRoute === 'history' && (
          <HistoryPage
            onSelectSession={handleSelectHistorySession}
            onStartInterview={handleStartInterview}
          />
        )}
      </main>

      <Footer />
    </div>
  );
}

