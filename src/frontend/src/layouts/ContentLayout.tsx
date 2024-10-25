import { Outlet } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import Navbar from "../components/Navbar";
import { SelectedTagsProvider } from "../contexts/SelectedTagsContext";

const MainLayout: React.FC = () => {
  return (
    <SelectedTagsProvider>
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <div className="flex-grow pt-24 bg-gradient-to-b from-blue-50 to-white">
        <Outlet/>
      </div>
      <ToastContainer />
    </div>
    </SelectedTagsProvider>
  );
};

export default MainLayout;
