import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Navbar from './components/Navbar';
import HomePage from './pages/HomePage';
import DocumentAnalysisPage from './pages/DocumentAnalysisPage';
import AnalysisResultsPage from './pages/AnalysisResultsPage';
import AboutPage from './pages/AboutPage';
import './index.css';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-legal-50">
        <Navbar />
        <main className="pt-16">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/analyze" element={<DocumentAnalysisPage />} />
            <Route path="/results" element={<AnalysisResultsPage />} />
            <Route path="/about" element={<AboutPage />} />
          </Routes>
        </main>
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: '#363636',
              color: '#fff',
            },
            success: {
              duration: 3000,
              iconTheme: {
                primary: '#16a34a',
                secondary: '#fff',
              },
            },
            error: {
              duration: 5000,
              iconTheme: {
                primary: '#dc2626',
                secondary: '#fff',
              },
            },
          }}
        />
      </div>
    </Router>
  );
}

export default App;
