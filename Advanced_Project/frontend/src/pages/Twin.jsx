import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { MessageSquare, Zap, Loader2, Send } from 'lucide-react';
import { chatWithTwin, simulateScenario } from '../lib/api';

export default function Twin() {
  const [mode, setMode] = useState('chat'); // 'chat' or 'simulate'
  
  // Chat state
  const [messages, setMessages] = useState([]);
  const [chatInput, setChatInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);

  // Simulate state
  const [scenarioInput, setScenarioInput] = useState('');
  const [isSimulating, setIsSimulating] = useState(false);
  const [simulationResult, setSimulationResult] = useState(null);

  const handleChat = async (e) => {
    e.preventDefault();
    if (!chatInput.trim()) return;
    
    const userMsg = { role: 'user', content: chatInput };
    setMessages(prev => [...prev, userMsg]);
    setChatInput('');
    setIsTyping(true);
    
    try {
      const data = await chatWithTwin(userMsg.content);
      setMessages(prev => [...prev, { role: 'twin', content: data.response }]);
    } catch (err) {
      console.error(err);
    } finally {
      setIsTyping(false);
    }
  };

  const handleSimulate = async (e) => {
    e.preventDefault();
    if (!scenarioInput.trim()) return;
    
    setIsSimulating(true);
    setSimulationResult(null);
    try {
      const data = await simulateScenario(scenarioInput);
      setSimulationResult(data.simulation);
    } catch (err) {
      console.error(err);
    } finally {
      setIsSimulating(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto h-[calc(100vh-100px)] flex flex-col">
      <header className="mb-6 flex space-x-4 border-b border-slate-800 pb-4">
        <button 
          onClick={() => setMode('chat')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-colors ${mode === 'chat' ? 'bg-primaryTeal/20 text-primaryTeal' : 'text-slate-400 hover:text-slate-200'}`}
        >
          <MessageSquare className="w-5 h-5" /> Chat with Twin
        </button>
        <button 
          onClick={() => setMode('simulate')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-colors ${mode === 'simulate' ? 'bg-secondaryPurple/20 text-secondaryPurple' : 'text-slate-400 hover:text-slate-200'}`}
        >
          <Zap className="w-5 h-5" /> Scenario Simulator
        </button>
      </header>

      {mode === 'chat' ? (
        <div className="flex-1 bg-slate-800/40 border border-slate-700 rounded-2xl flex flex-col overflow-hidden">
          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {messages.length === 0 && (
              <div className="text-center text-slate-500 mt-20">
                <MessageSquare className="w-12 h-12 mx-auto mb-4 opacity-50" />
                <p>Start a conversation with your digital twin.</p>
              </div>
            )}
            {messages.map((msg, idx) => (
              <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[80%] p-4 rounded-2xl ${msg.role === 'user' ? 'bg-primaryTeal text-slate-900 rounded-br-sm' : 'bg-slate-700 text-white rounded-bl-sm'}`}>
                  {msg.content}
                </div>
              </div>
            ))}
            {isTyping && (
              <div className="flex justify-start">
                <div className="bg-slate-700 text-white p-4 rounded-2xl rounded-bl-sm flex gap-2">
                  <span className="w-2 h-2 rounded-full bg-slate-400 animate-bounce"></span>
                  <span className="w-2 h-2 rounded-full bg-slate-400 animate-bounce" style={{ animationDelay: '0.2s' }}></span>
                  <span className="w-2 h-2 rounded-full bg-slate-400 animate-bounce" style={{ animationDelay: '0.4s' }}></span>
                </div>
              </div>
            )}
          </div>
          <form onSubmit={handleChat} className="p-4 bg-slate-900/50 border-t border-slate-700 flex gap-4">
            <input 
              type="text"
              value={chatInput}
              onChange={(e) => setChatInput(e.target.value)}
              placeholder="Say something to yourself..."
              className="flex-1 bg-slate-800 border-none focus:ring-2 focus:ring-primaryTeal rounded-xl px-4 py-3 text-white placeholder-slate-500"
            />
            <button disabled={isTyping || !chatInput.trim()} className="bg-primaryTeal text-slate-900 px-6 py-3 rounded-xl font-bold hover:bg-teal-400 disabled:opacity-50 transition-colors">
              <Send className="w-5 h-5" />
            </button>
          </form>
        </div>
      ) : (
        <div className="flex-1 flex flex-col gap-6 overflow-y-auto">
          <form onSubmit={handleSimulate} className="bg-slate-800/40 border border-slate-700 rounded-2xl p-6 shrink-0">
            <h3 className="text-xl font-bold mb-4">Test a Scenario</h3>
            <div className="flex gap-4">
              <input 
                type="text"
                value={scenarioInput}
                onChange={(e) => setScenarioInput(e.target.value)}
                placeholder="What would I do if I was offered a promotion but it required moving to a new city?"
                className="flex-1 bg-slate-900/50 border border-slate-700 focus:ring-2 focus:ring-secondaryPurple rounded-xl px-4 py-3 text-white"
              />
              <button disabled={isSimulating || !scenarioInput.trim()} className="bg-gradient-to-r from-secondaryPurple to-purple-400 text-white px-8 py-3 rounded-xl font-bold flex items-center gap-2 hover:opacity-90 disabled:opacity-50">
                {isSimulating ? <Loader2 className="w-5 h-5 animate-spin" /> : <Zap className="w-5 h-5" />}
                Simulate
              </button>
            </div>
          </form>

          {simulationResult && (
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-slate-800/40 border border-secondaryPurple/30 rounded-2xl p-6 relative overflow-hidden flex-1"
            >
              <div className="absolute top-0 left-0 w-1 p-full h-full bg-secondaryPurple"></div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8 h-full">
                <div>
                  <h4 className="text-secondaryPurple font-bold uppercase text-sm tracking-wider mb-4">Internal Reasoning</h4>
                  <div className="space-y-4">
                    {simulationResult.internal_reasoning?.map((step, idx) => (
                      <div key={idx} className="flex gap-3">
                        <span className="flex items-center justify-center w-6 h-6 rounded-full bg-slate-700 text-xs font-bold shrink-0">{idx + 1}</span>
                        <p className="text-slate-300">{step}</p>
                      </div>
                    ))}
                  </div>
                </div>
                
                <div className="space-y-8">
                  <div>
                    <h4 className="text-secondaryPurple font-bold uppercase text-sm tracking-wider mb-2">Emotional Reaction</h4>
                    <p className="bg-slate-900/50 p-4 rounded-xl text-slate-200 border border-slate-700/50">{simulationResult.emotional_reaction}</p>
                  </div>
                  <div>
                    <h4 className="text-secondaryPurple font-bold uppercase text-sm tracking-wider mb-2">Predicted Decision</h4>
                    <p className="bg-gradient-to-br from-slate-900 to-indigo-900/50 p-4 rounded-xl text-white border border-indigo-500/30 text-lg font-medium">{simulationResult.predicted_decision}</p>
                  </div>
                </div>
              </div>
            </motion.div>
          )}
        </div>
      )}
    </div>
  );
}
