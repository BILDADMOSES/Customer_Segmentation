import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import LandingPage from "./LandingPage";
import UploadPage from "./UploadPage";

// Header component
const Header = () => (
  <header className="bg-blue-500 p-4 text-white flex px-24 justify-between text-center">
    <h1 className="text-2xl font-bold">SmartSegmentor</h1>
    <nav className="mt-2 ">
      <Link to="/" className="mx-2">
        Home
      </Link>
      <Link to="/upload" className="mx-2">
        Upload
      </Link>
    </nav>
  </header>
);

// Footer component
const Footer = () => (
  <footer className="bg-gray-200 p-4 text-center">
    <p>&copy; 2023 SmartSegmentor. All rights reserved.</p>
  </footer>
);

// App component
function App() {
  return (
    <BrowserRouter>
      <div className="flex flex-col bg-gray-100 min-h-screen">
        <Header />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/upload" element={<UploadPage />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </BrowserRouter>
  );
}

export default App;
