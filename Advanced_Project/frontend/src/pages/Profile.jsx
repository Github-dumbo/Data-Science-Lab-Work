import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Activity, BrainCircuit } from 'lucide-react';
import { getProfile } from '../lib/api';

export default function Profile() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getProfile().then(data => {
      setProfile(data);
      setLoading(false);
    });
  }, []);

  if (loading) {
    return <div className="flex items-center justify-center h-full"><Activity className="w-8 h-8 animate-pulse text-primaryTeal" /></div>;
  }

  const traits = profile?.traits || {};

  return (
    <div className="max-w-4xl mx-auto pb-12">
      <header className="mb-10">
        <h2 className="text-3xl font-bold mb-2">Psychological Twin Profile</h2>
        <p className="text-slate-400">A comprehensive mapping of your thought patterns and emotional state.</p>
      </header>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Core Summary */}
        <motion.div 
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="bg-slate-800/40 border border-slate-700 rounded-2xl p-6"
        >
          <div className="flex items-center gap-3 mb-6">
            <div className="p-3 bg-slate-900 rounded-xl">
              <BrainCircuit className="w-6 h-6 text-primaryTeal" />
            </div>
            <h3 className="text-xl font-bold">Mind Summary</h3>
          </div>
          <p className="text-slate-300 leading-relaxed text-lg">
            {profile?.summary || "No data available. Go to the Home tab to share your thoughts."}
          </p>
        </motion.div>

        {/* Traits Visualization */}
        <motion.div 
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-slate-800/40 border border-slate-700 rounded-2xl p-6"
        >
          <h3 className="text-xl font-bold mb-6">Trait Metrics</h3>
          <div className="space-y-6">
             {Object.entries(traits).map(([trait, value], idx) => (
                <div key={idx} className="relative">
                  <div className="flex justify-between text-sm mb-2">
                    <span className="font-medium text-slate-200">{trait}</span>
                    <span className="text-primaryTeal font-bold">{value}%</span>
                  </div>
                  <div className="w-full h-3 bg-slate-900 rounded-full overflow-hidden">
                    <motion.div 
                      initial={{ width: 0 }}
                      animate={{ width: `${value}%` }}
                      transition={{ duration: 1, delay: 0.2 + (idx * 0.1) }}
                      className={`h-full rounded-full ${value > 60 ? 'bg-gradient-to-r from-purple-500 to-primaryTeal' : 'bg-gradient-to-r from-teal-500 to-green-400'}`}
                    />
                  </div>
                </div>
             ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
}
