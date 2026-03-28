import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Sparkles, Brain, Loader2 } from 'lucide-react';
import { analyzeInput } from '../lib/api';

export default function Home() {
  const [input, setInput] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    
    setIsAnalyzing(true);
    setResult(null);
    try {
      const data = await analyzeInput(input);
      setResult(data.profile);
      setInput('');
    } catch (err) {
      console.error(err);
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto flex flex-col items-center pt-20">
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-12"
      >
        <h1 className="text-4xl md:text-5xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-teal-400 to-purple-500">
          MindMirror™
        </h1>
        <p className="text-slate-400 text-lg">A version of you... built from your thoughts.</p>
      </motion.div>

      <motion.div 
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.1 }}
        className="w-full bg-slate-800/50 backdrop-blur-xl border border-slate-700/50 rounded-2xl p-6 shadow-2xl"
      >
        <form onSubmit={handleSubmit} className="relative">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="What's on your mind...? Share your thoughts, problems, or situations."
            disabled={isAnalyzing}
            className="w-full bg-slate-900/50 text-white placeholder-slate-500 rounded-xl p-4 min-h-[160px] resize-none focus:outline-none focus:ring-2 focus:ring-primaryTeal/50 transition-all disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={!input.trim() || isAnalyzing}
            className="absolute bottom-4 right-4 bg-gradient-to-r from-primaryTeal to-secondaryPurple text-white px-6 py-2 rounded-lg font-medium flex items-center gap-2 hover:opacity-90 transition-opacity disabled:opacity-50"
          >
            {isAnalyzing ? <Loader2 className="w-5 h-5 animate-spin" /> : <Send className="w-5 h-5" />}
            {isAnalyzing ? 'Analyzing...' : 'Send to Mind'}
          </button>
        </form>
      </motion.div>

      <AnimatePresence>
        {result && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="w-full mt-8"
          >
            <div className="bg-slate-800/80 border border-primaryTeal/30 rounded-2xl p-6 relative overflow-hidden group">
              <div className="absolute top-0 left-0 w-1 p-full h-full bg-gradient-to-b from-primaryTeal to-secondaryPurple"></div>
              <h3 className="text-xl font-bold flex items-center gap-2 text-primaryTeal mb-4">
                <Sparkles className="w-5 h-5" /> Profile Updated
              </h3>
              <p className="text-slate-300 mb-6">{result.summary}</p>
              
              <div className="space-y-4">
                <h4 className="text-sm font-semibold text-slate-400 uppercase tracking-wider">New Insights</h4>
                {result.new_insights?.map((insight, idx) => (
                  <div key={idx} className="flex items-start gap-3 bg-slate-900/50 p-4 rounded-xl">
                    <Brain className="w-5 h-5 text-secondaryPurple shrink-0 mt-0.5" />
                    <p className="text-slate-200">{insight}</p>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
