import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';
import './App.css';

const API_BASE = 'http://localhost:8000';

function App() {
  const [metrics, setMetrics] = useState({});
  const [prediction, setPrediction] = useState(null);
  const [data, setData] = useState([]);
  const [gpa, setGpa] = useState(8.0);
  const [testScore, setTestScore] = useState(80);
  const [experience, setExperience] = useState(0);

  useEffect(() => {
    fetchMetrics();
    fetchData();
  }, []);

  const fetchMetrics = async () => {
    const res = await axios.get(`${API_BASE}/metrics`);
    setMetrics(res.data);
  };

  const fetchData = async () => {
    const res = await axios.get(`${API_BASE}/data`);
    setData(res.data);
  };

  const predictPlacement = async () => {
    const res = await axios.get(`${API_BASE}/predict`, {
      params: { gpa, test_score: testScore, work_experience: experience }
    });
    setPrediction(res.data.placement_probability);
  };

  const branchData = data.reduce((acc, student) => {
    acc[student.branch] = (acc[student.branch] || 0) + 1;
    return acc;
  }, {});

  return (
    <div className="App">
      <header className="header">
        <h1>🎓 Placement Metrics Dashboard</h1>
      </header>

      <div className="metrics-grid">
        <div className="metric-card">
          <h3>Total Students</h3>
          <div className="metric-value">{metrics.total_students}</div>
        </div>
        <div className="metric-card">
          <h3>Placement Rate</h3>
          <div className="metric-value">{metrics.placement_rate}%</div>
        </div>
        <div className="metric-card">
          <h3>Avg Package</h3>
          <div className="metric-value">₹{metrics.avg_package}L</div>
        </div>
        <div className="metric-card">
          <h3>Top Recruiter</h3>
          <div className="metric-value">{metrics.top_company}</div>
        </div>
      </div>

      <div className="charts-grid">
        <div className="chart-card">
          <h3>Branch Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={Object.entries(branchData).map(([name, value]) => ({name, value}))}>
              <Bar dataKey="value" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="predictor-section">
        <h2>🔮 ML Placement Predictor</h2>
        <div className="predictor-form">
          <input
            type="number"
            placeholder="GPA (0-10)"
            value={gpa}
            onChange={(e) => setGpa(parseFloat(e.target.value))}
            min="0"
            max="10"
            step="0.1"
          />
          <input
            type="number"
            placeholder="Test Score (0-100)"
            value={testScore}
            onChange={(e) => setTestScore(parseInt(e.target.value))}
            min="0"
            max="100"
          />
          <input
            type="number"
            placeholder="Experience (years)"
            value={experience}
            onChange={(e) => setExperience(parseInt(e.target.value))}
            min="0"
            max="10"
          />
          <button onClick={predictPlacement}>Predict</button>
        </div>
        {prediction && (
          <div className="prediction-result">
            Placement Probability: <strong>{(prediction * 100).toFixed(1)}%</strong>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
