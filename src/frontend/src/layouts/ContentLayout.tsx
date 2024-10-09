import { Outlet } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import Navbar from "../components/Navbar";

const MainLayout = () => {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Navbar stays fixed at the top */}
      <Navbar />
      {/* Content area below the Navbar */}
      <div className="flex-grow pt-24 bg-gradient-to-b from-blue-50 to-white">
        <Outlet />
      </div>
      <ToastContainer />
    </div>
  );
};

export default MainLayout;
