// Install required dependencies: npm install axios react-dropzone
import React, { useState } from 'react';
import axios from 'axios';
import { useDropzone } from 'react-dropzone';

const UploadPage = () => {
  const [file, setFile] = useState(null);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const onDrop = (acceptedFiles) => {
    setFile(acceptedFiles[0]);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  const handleUpload = async () => {
    if (!file) {
      alert('Please upload a CSV file');
      return;
    }

    setLoading(true);

    try {
      const formData = new FormData();
      formData.append('csvFile', file);

      // Replace 'YOUR_API_ENDPOINT' with the actual endpoint for file upload
      const response = await axios.post('YOUR_API_ENDPOINT', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setData(response.data);
    } catch (error) {
      console.error('Error uploading file:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded shadow-md w-full max-w-md">
        <div {...getRootProps()} className={`dropzone ${isDragActive && 'active'}`}>
          <input {...getInputProps()} />
          <p className="text-gray-600">
            Drag 'n' drop a CSV file here, or click to select one
          </p>
        </div>
        <button
          onClick={handleUpload}
          className="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          {loading ? 'Uploading...' : 'Upload'}
        </button>
        {data && (
          <div className="mt-8">
            <h2 className="text-xl font-semibold mb-4">Uploaded Data Details:</h2>
            {/* Display the details and images from the server response */}
            {/* Adjust the structure based on the actual response structure */}
            <div>
              <p>Details: {data.details}</p>
              <img src={data.image1} alt="Image 1" className="mt-2" />
              <img src={data.image2} alt="Image 2" className="mt-2" />
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default UploadPage;
