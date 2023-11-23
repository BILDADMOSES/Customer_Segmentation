import { Link } from "react-router-dom";
import "./styles.css";

const LandingPage = () => {
  return (
    <div className="min-h-[550px] flex px-24 flex-col items-center justify-center bg-gray-100">
      <div className="text-center">
        <h1 className="text-4xl font-extrabold text-gray-800 mb-4">
          Customer Segmentation Service
        </h1>
        <p className="text-lg text-gray-600 mb-8">
          Customer segmentation is the process of dividing a customer base into
          groups of individuals with similar characteristics, such as
          demographics, behavior, and purchase history. Our advanced customer
          segmentation tool leverages machine learning techniques to provide
          businesses with valuable insights and strategic advantages. With this
          tool, businesses can:
        </p>
        <ul className="text-left flex flex-col items-center text-gray-700 mb-8">
          <li>- Customize marketing strategies for each segment.</li>
          <li>- Improve customer retention and loyalty.</li>
          <li>- Optimize product recommendations.</li>
          <li>- Enhance the overall customer experience.</li>
        </ul>
        <Link to="/upload" className="text-blue-500 hover:underline">
          <button className="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            Try It Out
          </button>
        </Link>
      </div>
    </div>
  );
};

export default LandingPage;
