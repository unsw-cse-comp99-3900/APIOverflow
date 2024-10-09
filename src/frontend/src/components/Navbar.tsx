import { NavLink } from "react-router-dom";
import logo from "../assets/images/logo.svg";
import { FaUserCircle } from "react-icons/fa"; // Import the user icon

const Navbar = () => {
  const linkClass = ({ isActive }: { isActive: boolean }) =>
    isActive
      ? "bg-white text-blue-900 hover:bg-gray-100 hover:text-bg-blue-900 rounded-md flex items-center justify-center h-12 w-auto px-4 py-2"
      : "text-white hover:bg-white hover:text-blue-900 rounded-md flex items-center justify-center h-12 w-auto px-4 py-2";

  return (
    <nav className="bg-blue-900 border-b border-gray-100 fixed top-0 w-full z-50 ">
      <div className="m-auto px-20">
        <div className="flex h-24 items-center justify-between">
          <div className="flex flex-1 items-center justify-center md:items-stretch md:justify-start">
            <NavLink className="flex flex-shrink-0 items-center mr-4" to="/">
              <img className="h-10 w-auto" src={logo} alt="React Jobs" />
              <span className="hidden md:block text-white text-2xl font-bold ml-2">
                API Overflow
              </span>
            </NavLink>

            <div className="ml-auto">
              <div className="flex items-center space-x-4">
                <NavLink to="/" className={linkClass}>
                  <strong>Home</strong>
                </NavLink>
                <NavLink to="/apis" className={linkClass}>
                  <strong>APIs</strong>
                </NavLink>
                <NavLink to="/profile/add-api" className={linkClass}>
                  <strong>Add API</strong>
                </NavLink>
                <NavLink to='/login' className={linkClass}>
                  <strong>Login</strong>
                </NavLink>
                <NavLink to="/profile/my-apis" className={linkClass}>
                  <span className="flex items-center space-x-2">
                  <FaUserCircle className={`h-8 w-8 ${{ linkClass }}`} />
                    <strong>My Profile</strong>
                  </span>
                </NavLink>

              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
