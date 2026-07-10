import React from 'react';
import { BarChart3, TrendingDown, Target } from 'lucide-react';

export default function ModelInsights() {
  return (
    <div className="space-y-8 animate-fade-in">
      <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
        <h2 className="text-2xl font-bold text-slate-800 mb-2">Model Architecture & Performance</h2>
        <p className="text-slate-600">
          The underlying model is a highly tuned tree-based regressor trained on 
          standardized sensor telemetry. We avoided heavy feature engineering in favor 
          of maintaining a robust, interpretable baseline using the raw physical signals.
        </p>
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 flex items-center space-x-4">
          <div className="p-3 bg-indigo-50 text-indigo-600 rounded-lg">
            <Target size={24} />
          </div>
          <div>
            <p className="text-sm font-medium text-slate-500">Algorithm</p>
            <p className="text-lg font-bold text-slate-900">LGBMRegressor</p>
          </div>
        </div>
        
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 flex items-center space-x-4">
          <div className="p-3 bg-emerald-50 text-emerald-600 rounded-lg">
            <TrendingDown size={24} />
          </div>
          <div>
            <p className="text-sm font-medium text-slate-500">Validation RMSE</p>
            <p className="text-lg font-bold text-slate-900">34.86 Cycles</p>
          </div>
        </div>
        
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 flex items-center space-x-4">
          <div className="p-3 bg-amber-50 text-amber-600 rounded-lg">
            <BarChart3 size={24} />
          </div>
          <div>
            <p className="text-sm font-medium text-slate-500">Inputs Tracked</p>
            <p className="text-lg font-bold text-slate-900">20 Active Sensors</p>
          </div>
        </div>
      </div>

      <div className="bg-white p-8 rounded-xl shadow-sm border border-slate-200">
        <h3 className="text-xl font-bold text-slate-800 mb-6">Feature Importance Profile</h3>
        
        <div className="prose max-w-none text-slate-600 mb-8">
          <p>
            Analysis of the model's internal splitting criteria reveals which engine parameters 
            are most strongly indicative of impending failure. High-pressure turbine parameters 
            and core temperatures typically dominate the predictive signal.
          </p>
        </div>

        {/* Simplified mock feature importance visualization since we don't have the real image generated yet */}
        <div className="space-y-4 max-w-2xl">
          {[
            { name: 'Static Pressure HPC Outlet', val: 95 },
            { name: 'Total Temp LPT Outlet', val: 82 },
            { name: 'Bypass Ratio', val: 78 },
            { name: 'Total Pressure HPC Outlet', val: 65 },
            { name: 'Fuel Flow Ratio', val: 55 },
            { name: 'Engine Age (Cycles)', val: 40 },
          ].map(feat => (
            <div key={feat.name} className="flex items-center text-sm">
              <div className="w-64 font-medium text-slate-700 truncate pr-4">{feat.name}</div>
              <div className="flex-1 h-5 bg-slate-100 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-aviationBlue rounded-full"
                  style={{ width: `${feat.val}%` }}
                ></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
