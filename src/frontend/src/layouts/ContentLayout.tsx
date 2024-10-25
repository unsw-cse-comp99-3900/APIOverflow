import { Outlet } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import Navbar from "../components/Navbar";
import { useState } from "react";

const MainLayout: React.FC = () => {
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <div className="flex-grow pt-24 bg-gradient-to-b from-blue-50 to-white">
        <Outlet context={{ selectedTags, setSelectedTags }} />
      </div>
      <ToastContainer />
    </div>
  );
};

export default MainLayout;
