// LandingPage.jsx

import React from 'react';
import { Link } from 'react-router-dom';
import UploadPage from './UploadPage';
import './styles.css';

const LandingPage = () => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
      <div className="text-center">
        <h1 className="text-4xl font-extrabold text-gray-800 mb-4">
          Customer Segmentation Service
        </h1>
        <p className="text-lg text-gray-600 mb-8">
          Better serve different demographics with our advanced customer segmentation tool.
        </p>
        <Link to="/upload" className="text-blue-500 hover:underline">
          Go to Upload Page
        </Link>
      </div>
      <footer className="mt-8 text-center text-gray-500">
        &copy; 2023 Your Company Name. All rights reserved.
      </footer>
    </div>
  );
};

export default LandingPage;
