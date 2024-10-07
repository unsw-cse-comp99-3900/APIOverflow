import { NavLink } from 'react-router-dom';
import logo from '../assets/images/logo.svg';

const Navbar = () => {
  const linkClass = ({ isActive }: { isActive: boolean }) =>
    isActive
      ? 'bg-white text-blue-900 hover:bg-gray-100 hover:text-bg-blue-900 rounded-md px-3 py-2'
      : 'text-white hover:bg-white hover:text-blue-900 rounded-md px-3 py-2';

  return (
    <nav className='bg-blue-900 border-b border-gray-100'>
      <div className='mx-auto max-w-7xl px-2 sm:px-6 lg:px-8'>
        <div className='flex h-20 items-center justify-between'>
          <div className='flex flex-1 items-center justify-center md:items-stretch md:justify-start'>
            <NavLink className='flex flex-shrink-0 items-center mr-4' to='/'>
              <img className='h-10 w-auto' src={logo} alt='React Jobs' />
              <span className='hidden md:block text-white text-2xl font-bold ml-2'>
                API Overflow
              </span>
            </NavLink>
            <div className='md:ml-auto'>
              <div className='flex space-x-2'>
                <NavLink to='/' className={linkClass}>
                <strong>Home</strong>
                </NavLink>
                <NavLink to='/apis' className={linkClass}>
                <strong>APIs</strong>
                </NavLink>
                <NavLink to='/add-api' className={linkClass}>
                <strong>Add API</strong>
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
