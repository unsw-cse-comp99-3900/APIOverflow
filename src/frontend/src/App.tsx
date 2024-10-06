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
// import { apiLoader } from './utils/loaders';
import EditApiPage from './pages/EditApiPage';
import CategoriesPage from './pages/CategoriesPage';

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
          element={<ApiPage />}
        />
      </Route>
    )
      
  );
  return <RouterProvider router={router} />;
}

export default App;