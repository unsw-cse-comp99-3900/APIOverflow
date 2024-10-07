import {
  Route,
  createBrowserRouter,
  createRoutesFromElements,
  RouterProvider,
} from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import HomePage from './pages/HomePage';
import APIsPage from './pages/ApisPage';
import AddApiPage from './pages/AddApiPage';
import ApiPage from './pages/ApiPage';
import EditApiPage from './pages/EditApiPage';
import CategoriesPage from './pages/CategoriesPage';
import { deleteApi } from './services/apiServices';
import { apiLoader } from './utils/loaders';
import Login from './components/Login';  // Import Login component


const App = () => {
  const router = createBrowserRouter(
    createRoutesFromElements(
      <Route path='/' element={<MainLayout />}>
        <Route index element={<HomePage />} />
        <Route path='/apis' element={<APIsPage />} />
        <Route path='/add-api' element={<AddApiPage />} />
        <Route path='/edit-api' element={<EditApiPage />} />
        <Route path='/categories' element={<CategoriesPage />} />
        <Route
          path='/apis/:id' 
          element={<ApiPage deleteApi={deleteApi} />}
          loader={apiLoader}
        />
        {/* Add the login route */}
        <Route path='/login' element={<Login />} />
      </Route>
    )
  );
  
  return <RouterProvider router={router} />;
}

export default App;
