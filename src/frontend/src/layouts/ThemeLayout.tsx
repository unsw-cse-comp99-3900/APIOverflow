import { Outlet } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import Navbar from "../components/Navbar";

const ThemeLayout = () => {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Navbar stays fixed at the top */}
      <Navbar />
      {/* Content area below the Navbar */}
        <Outlet />
      <ToastContainer />
    </div>
  );
};

export default ThemeLayout;
