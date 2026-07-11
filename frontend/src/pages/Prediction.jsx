import React, { useState } from 'react';
import axios from 'axios';
import { Plane, AlertTriangle, CheckCircle, XCircle, Gauge } from 'lucide-react';

// The exact sensors active in the PRD 1 model
const ACTIVE_SENSORS = [
    'sensor_1', 'sensor_2', 'sensor_3', 'sensor_4', 'sensor_5', 'sensor_6',
    'sensor_7', 'sensor_8', 'sensor_9', 'sensor_10', 'sensor_11', 'sensor_12',
    'sensor_13', 'sensor_14', 'sensor_15', 'sensor_17', 'sensor_18', 'sensor_19',
    'sensor_20', 'sensor_21'
];

const SENSOR_MAP = {
  'cycle': { label: 'Current Cycle', desc: 'Engine age in flight cycles' },
  'op_setting_1': { label: 'Op Setting 1', desc: 'Altitude/Mach parameter' },
  'op_setting_2': { label: 'Op Setting 2', desc: 'Altitude/Mach parameter' },
  'op_setting_3': { label: 'Op Setting 3', desc: 'TRA (Throttle Resolver Angle)' },
  'sensor_1': { label: 'Total Temp Fan Inlet', desc: 'Temperature at fan inlet (°R)' },
  'sensor_2': { label: 'Total Temp LPC Outlet', desc: 'Temperature at LPC outlet (°R)' },
  'sensor_3': { label: 'Total Temp HPC Outlet', desc: 'Temperature at HPC outlet (°R)' },
  'sensor_4': { label: 'Total Temp LPT Outlet', desc: 'Temperature at LPT outlet (°R)' },
  'sensor_5': { label: 'Pressure Fan Inlet', desc: 'Pressure at fan inlet (psia)' },
  'sensor_6': { label: 'Total Pressure Bypass', desc: 'Total pressure in bypass-duct (psia)' },
  'sensor_7': { label: 'Total Pressure HPC Outlet', desc: 'Total pressure at HPC outlet (psia)' },
  'sensor_8': { label: 'Physical Fan Speed', desc: 'Physical fan speed (rpm)' },
  'sensor_9': { label: 'Physical Core Speed', desc: 'Physical core speed (rpm)' },
  'sensor_10': { label: 'Engine Pressure Ratio', desc: 'Engine pressure ratio (P50/P2)' },
  'sensor_11': { label: 'Static Pressure HPC Outlet', desc: 'Static pressure at HPC outlet (psia)' },
  'sensor_12': { label: 'Fuel Flow Ratio', desc: 'Ratio of fuel flow to Ps30 (pps/psia)' },
  'sensor_13': { label: 'Corrected Fan Speed', desc: 'Corrected fan speed (rpm)' },
  'sensor_14': { label: 'Corrected Core Speed', desc: 'Corrected core speed (rpm)' },
  'sensor_15': { label: 'Bypass Ratio', desc: 'Bypass Ratio' },
  'sensor_17': { label: 'Bleed Enthalpy', desc: 'Bleed Enthalpy' },
  'sensor_18': { label: 'Demanded Fan Speed', desc: 'Demanded fan speed (rpm)' },
  'sensor_19': { label: 'Demanded Corrected Fan Speed', desc: 'Demanded corrected fan speed (rpm)' },
  'sensor_20': { label: 'HPT Coolant Bleed', desc: 'HPT coolant bleed (lbm/s)' },
  'sensor_21': { label: 'LPT Coolant Bleed', desc: 'LPT coolant bleed (lbm/s)' }
};

export default function Prediction() {
  const [formData, setFormData] = useState({
    cycle: 120,
    op_setting_1: 20.0,
    op_setting_2: 0.7,
    op_setting_3: 100.0,
    sensor_1: 518.67,
    sensor_2: 642.0,
    sensor_3: 1589.0,
    sensor_4: 1400.0,
    sensor_5: 14.62,
    sensor_6: 21.61,
    sensor_7: 554.0,
    sensor_8: 2388.0,
    sensor_9: 9050.0,
    sensor_10: 1.3,
    sensor_11: 47.0,
    sensor_12: 521.0,
    sensor_13: 2388.0,
    sensor_14: 8130.0,
    sensor_15: 8.4,
    sensor_17: 393.0,
    sensor_18: 2388.0,
    sensor_19: 100.0,
    sensor_20: 38.9,
    sensor_21: 23.3
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [samples, setSamples] = useState([]);

  // API configuration for dynamic deployment
  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  React.useEffect(() => {
    // Load sample engines from backend
    axios.get(`${API_URL}/sample-engines`)
      .then(res => setSamples(res.data))
      .catch(err => console.error("Could not load samples:", err));
  }, []);

  const handleSampleSelect = (e) => {
    const idx = e.target.value;
    if (idx !== "") {
      const sampleData = samples[idx].data;
      setFormData(prev => ({
        ...prev,
        ...sampleData
      }));
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: parseFloat(value) || 0 }));
  };

  const handlePredict = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      // Send request to backend using dynamic URL
      const response = await axios.post(`${API_URL}/predict`, formData);
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to connect to the prediction API.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto grid md:grid-cols-3 gap-8 animate-fade-in">
      {/* Input Form */}
      <div className="md:col-span-2 bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <div className="flex items-center justify-between mb-6 border-b pb-4">
          <div className="flex items-center space-x-3">
            <Gauge className="text-aviationBlue" size={24} />
            <h2 className="text-2xl font-bold text-slate-800">Engine Telemetry Input</h2>
          </div>
          
          {samples.length > 0 && (
            <select 
              onChange={handleSampleSelect}
              className="text-sm border-slate-300 rounded-md shadow-sm p-2 border focus:ring-aviationBlue focus:border-aviationBlue bg-slate-50"
              defaultValue=""
            >
              <option value="" disabled>Autofill from Test Data...</option>
              {samples.map((s, idx) => (
                <option key={idx} value={idx}>{s.name}</option>
              ))}
            </select>
          )}
        </div>
        
        <form onSubmit={handlePredict} className="space-y-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="col-span-2 md:col-span-4 bg-slate-50 p-4 rounded-lg border border-slate-100">
              <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-3">Operational State</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {['cycle', 'op_setting_1', 'op_setting_2', 'op_setting_3'].map(field => (
                  <div key={field} title={SENSOR_MAP[field]?.desc || ''}>
                    <label className="block text-xs font-medium text-slate-700 mb-1">{SENSOR_MAP[field]?.label || field}</label>
                    <input type="number" step={field === 'cycle' ? '1' : '0.001'} name={field} value={formData[field]} onChange={handleChange} className="w-full border-slate-300 rounded-md shadow-sm text-sm p-2 border focus:ring-aviationBlue focus:border-aviationBlue" />
                  </div>
                ))}
              </div>
            </div>

            <div className="col-span-2 md:col-span-4 mt-2">
              <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-3">Active Sensor Readings</h3>
              <div className="grid grid-cols-3 md:grid-cols-4 gap-4">
                {ACTIVE_SENSORS.map(sensor => (
                  <div key={sensor} title={SENSOR_MAP[sensor]?.desc || ''}>
                    <label className="block text-xs font-medium text-slate-700 mb-1">{SENSOR_MAP[sensor]?.label || sensor}</label>
                    <input type="number" step="0.1" name={sensor} value={formData[sensor]} onChange={handleChange} className="w-full border-slate-300 rounded-md shadow-sm text-sm p-2 border focus:ring-aviationBlue focus:border-aviationBlue" />
                  </div>
                ))}
              </div>
            </div>
          </div>

          <button 
            type="submit" 
            disabled={loading}
            className="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-aviationBlue hover:bg-blue-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-aviationBlue transition-colors disabled:bg-slate-400"
          >
            {loading ? 'Analyzing Telemetry...' : 'Predict Remaining Useful Life'}
          </button>
        </form>
      </div>

      {/* Results Panel */}
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 flex flex-col items-center justify-center text-center">
        {error && (
          <div className="text-red-500 flex flex-col items-center">
            <XCircle size={48} className="mb-2" />
            <p className="text-sm font-medium">{error}</p>
          </div>
        )}

        {!result && !error && (
          <div className="text-slate-400 flex flex-col items-center space-y-4">
            <Plane size={64} className="opacity-20" />
            <p className="text-sm">Submit telemetry data to generate an engine health prediction.</p>
          </div>
        )}

        {result && !error && (
          <div className="w-full animate-fade-in">
            <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-6">Prediction Results</h3>
            
            <div className="mb-8">
              <div className="text-6xl font-extrabold text-slate-900 mb-2">
                {Math.floor(result.predicted_rul)}
              </div>
              <div className="text-slate-500 font-medium">Predicted Remaining Useful Life (Flight Cycles)</div>
            </div>

            <div className={`p-4 rounded-lg flex flex-col items-center justify-center space-y-2 border
              ${result.status === 'Healthy' ? 'bg-emerald-50 border-emerald-200 text-emerald-700' : 
                result.status === 'Warning' ? 'bg-amber-50 border-amber-200 text-amber-700' : 
                'bg-red-50 border-red-200 text-red-700'}
            `}>
              <div className="flex items-center space-x-2">
                  {result.status === 'Healthy' ? <CheckCircle /> : <AlertTriangle />}
                  <span className="font-bold text-lg uppercase tracking-wide">Status: {result.status}</span>
              </div>
              <span className="text-sm font-medium text-center">
                  {result.status === 'Healthy' && "Maintenance not immediately required."}
                  {result.status === 'Warning' && "Inspection recommended during the next maintenance window."}
                  {result.status === 'Critical' && "Immediate maintenance is recommended."}
              </span>
            </div>
            
            <div className="mt-8 pt-6 border-t border-slate-100 w-full text-left">
                <h4 className="font-bold text-slate-800 mb-3 text-sm uppercase tracking-wide">Key Factors Considered</h4>
                <ul className="text-sm text-slate-600 list-disc list-inside space-y-1">
                    <li>Engine Age (Current Cycle)</li>
                    <li>Static Pressure HPC Outlet (Ps30)</li>
                    <li>Bypass Ratio (BPR)</li>
                    <li>Corrected Fan Speed (NRf)</li>
                    <li>Total Temperature LPT Outlet (T50)</li>
                </ul>
            </div>
            
            <p className="text-xs text-slate-400 mt-6">
              *Predictions are generated based on historical CMAPSS FD002 degradation profiles.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
