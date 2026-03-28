import React from 'react';
import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom';
import { Home, Brain, Activity, Settings } from 'lucide-react';
import HomePage from './pages/Home';
import ProfilePage from './pages/Profile';
import TwinPage from './pages/Twin';

function DashboardLayout({ children }) {
  return (
    <div className="flex h-screen w-full bg-darkBg text-white overflow-hidden">
      {/* Sidebar */}
      <nav className="w-64 border-r border-slate-800 bg-slate-900/50 p-6 flex flex-col gap-6">
        <div className="flex items-center gap-3 mb-8">
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primaryTeal to-secondaryPurple flex items-center justify-center">
            <Brain className="w-5 h-5 text-white" />
          </div>
          <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-teal-400 to-purple-500">
            MindMirror™
          </h1>
        </div>
        
        <div className="flex flex-col gap-2">
          <Link to="/" className="flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-slate-800 transition-colors text-slate-300 hover:text-white">
            <Home className="w-5 h-5" /> Home & Input
          </Link>
          <Link to="/profile" className="flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-slate-800 transition-colors text-slate-300 hover:text-white">
            <Activity className="w-5 h-5" /> Insights Profile
          </Link>
          <Link to="/twin" className="flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-slate-800 transition-colors text-slate-300 hover:text-white">
            <Brain className="w-5 h-5" /> Twin Simulation
          </Link>
        </div>
      </nav>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto p-8 relative">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,_var(--tw-gradient-stops))] from-teal-900/20 via-transparent to-transparent pointer-events-none" />
        <div className="relative z-10 h-full">
          {children}
        </div>
      </main>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <DashboardLayout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/profile" element={<ProfilePage />} />
          <Route path="/twin" element={<TwinPage />} />
        </Routes>
      </DashboardLayout>
    </BrowserRouter>
  );
}

export default App;
