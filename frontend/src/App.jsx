import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import Prediction from './pages/Prediction';
import ModelInsights from './pages/ModelInsights';

function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col bg-slate-50">
        <nav className="bg-aviationBlue text-white shadow-md">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-16">
              <div className="flex items-center space-x-4">
                <span className="font-bold text-xl tracking-tight">Engine Life Analysis</span>
                <div className="hidden md:flex space-x-4 ml-6">
                  <Link to="/" className="hover:bg-blue-800 px-3 py-2 rounded-md text-sm font-medium transition-colors">Overview</Link>
                  <Link to="/predict" className="hover:bg-blue-800 px-3 py-2 rounded-md text-sm font-medium transition-colors">Prediction Dashboard</Link>
                  <Link to="/insights" className="hover:bg-blue-800 px-3 py-2 rounded-md text-sm font-medium transition-colors">Model Insights</Link>
                </div>
              </div>
            </div>
          </div>
        </nav>
        
        <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/predict" element={<Prediction />} />
            <Route path="/insights" element={<ModelInsights />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
