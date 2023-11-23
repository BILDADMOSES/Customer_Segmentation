// App.jsx

import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LandingPage from './LandingPage';
import UploadPage from './UploadPage';
import './styles.css';

const App = () => {
  return (
    <Router>
        <Routes>
        <Route path="/" element={LandingPage} />
        <Route path="/upload" element={UploadPage} />
        </Routes>
    </Router>
  );
};

export default App;
