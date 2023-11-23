import { useState } from "react";
import axios from "axios";
import { useDropzone } from "react-dropzone";
import JSZip from "jszip";

const UploadPage = () => {
  const [file, setFile] = useState(null);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [imageUrls, setImageUrls] = useState(null);

  const onDrop = (acceptedFiles) => {
    setFile(acceptedFiles[0]);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  const handleUpload = async () => {
    if (!file) {
      alert("Please upload a CSV file");
      return;
    }
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("file", file);

      // Upload CSV file
      const uploadResponse = await axios.post(
        "http://127.0.0.1:8000/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setData(uploadResponse.data);
    } catch (error) {
      console.error("Error uploading file:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleProcessData = async () => {
    setLoading(true);

    try {
      // Fetch processed data (assuming it returns a zip file containing images)
      const processDataResponse = await axios.get(
        "http://127.0.0.1:8000/process-data",
        {
          responseType: "arraybuffer", // Ensure the response is treated as an array buffer
        }
      );

      // Unzip the received file
      const zip = new JSZip();
      const unzippedData = await zip.loadAsync(processDataResponse.data);

      // Extract image URLs
      const extractedImageUrls = [];
      for (const [relativePath, file] of Object.entries(unzippedData.files)) {
        const imageUrl = URL.createObjectURL(
          new Blob([await file.async("blob")], { type: file._data.mimeType })
        );
        extractedImageUrls.push(imageUrl);
      }

      setImageUrls(extractedImageUrls);
    } catch (error) {
      console.error("Error processing data:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[550px] flex-col flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded shadow-md w-full max-w-md">
        <div
          {...getRootProps()}
          className={`dropzone ${isDragActive && "active"}`}
        >
          <input {...getInputProps()} />
          <p className="text-gray-600">
            {file
              ? `File: ${file.name}`
              : "Drag and drop a CSV file here, or click to select one"}
          </p>
        </div>
        <button
          onClick={handleUpload}
          className="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          {loading ? "Uploading..." : "Upload"}
        </button>
        {data && (
          <div className="mt-8">
            <h2 className="text-xl font-semibold mb-4">
              Uploaded Data Details:
            </h2>
            <div>
              <p>Details: {data.details}</p>
              <button
                onClick={handleProcessData}
                className="mt-4 bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
              >
                {loading ? "Processing..." : "Process Data"}
              </button>
            </div>
          </div>
        )}
      </div>
      <div className="grid w-full ">
        {imageUrls && (
          <div className="my-8 px-24">
            <h2 className="text-xl font-semibold mb-4">Processed Images:</h2>
            <div className="grid grid-cols-4">
              {imageUrls.map((imageUrl, index) => (
                <img
                  key={index}
                  src={imageUrl}
                  alt={`Image ${index + 1}`}
                  className="mt-2 w-64"
                />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default UploadPage;
