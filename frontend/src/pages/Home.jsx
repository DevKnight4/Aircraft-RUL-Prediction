import React from 'react';
import { ShieldAlert, Activity, FileDigit } from 'lucide-react';

export default function Home() {
  return (
    <div className="space-y-8">
      <div className="bg-white p-8 rounded-xl shadow-sm border border-slate-200">
        <h1 className="text-4xl font-extrabold text-slate-900 tracking-tight mb-4">
          Aircraft Engine Remaining Useful Life Prediction
        </h1>
        <p className="text-lg text-slate-600 max-w-3xl leading-relaxed">
          An end-to-end machine learning system for predictive maintenance using NASA's CMAPSS turbofan engine dataset.
        </p>
      </div>
      
      <div className="grid md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 flex flex-col items-center text-center">
          <div className="bg-blue-50 p-4 rounded-full mb-4 text-aviationBlue">
            <FileDigit size={32} />
          </div>
          <h3 className="font-bold text-lg mb-2 text-slate-800">The Dataset</h3>
          <p className="text-slate-600 text-sm">
            Trained on NASA's CMAPSS FD002 dataset, comprising thousands of flight cycles 
            and complex multi-sensor degradation trajectories across varying conditions.
          </p>
        </div>
        
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 flex flex-col items-center text-center">
          <div className="bg-blue-50 p-4 rounded-full mb-4 text-aviationBlue">
            <Activity size={32} />
          </div>
          <h3 className="font-bold text-lg mb-2 text-slate-800">The Model</h3>
          <p className="text-slate-600 text-sm">
            Powered by a tuned LightGBM regressor trained on the CMAPSS dataset to find degradation patterns in raw sensor noise.
          </p>
        </div>
        
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 flex flex-col items-center text-center">
          <div className="bg-blue-50 p-4 rounded-full mb-4 text-aviationBlue">
            <ShieldAlert size={32} />
          </div>
          <h3 className="font-bold text-lg mb-2 text-slate-800">The Goal</h3>
          <p className="text-slate-600 text-sm">
            Assist maintenance teams in scheduling inspections before engines approach end-of-life using Remaining Useful Life predictions.
          </p>
        </div>
      </div>
    </div>
  );
}
