import {
  Route,
  createBrowserRouter,
  createRoutesFromElements,
  RouterProvider,
} from "react-router-dom";
import MainLayout from "./layouts/MainLayout";
import UserProfileLayout from "./layouts/UserProfileLayout";
import HomePage from "./pages/HomePage";
import APIsPage from "./pages/ApisPage";
import AddApiPage from "./pages/AddApiPage";
import ApiPage from "./pages/ApiPage";
import EditApiPage from "./pages/EditApiPage";
import MyApisPage from "./pages/MyApisPage";
import MyApiPage from "./pages/MyApiPage";

const App = () => {
  const router = createBrowserRouter(
    createRoutesFromElements(
      <Route path="/" element={<MainLayout />}>
        <Route index element={<HomePage />} />
        <Route path="/apis" element={<APIsPage />} />
        <Route path="/apis/:id" element={<ApiPage />} />

        <Route path="/edit-api" element={<EditApiPage />} />

        <Route path="/profile" element={<UserProfileLayout />}>
          <Route path="/profile/my-apis" element={<MyApisPage />} />
          <Route path="/profile/my-apis/:id" element={<MyApiPage />} />
          <Route path="/profile/add-api" element={<AddApiPage />} />
          <Route path="/profile/my-apis/:id/edit" element={<EditApiPage/>} />
        </Route>
      </Route>
    )
  );
  return <RouterProvider router={router} />;
};

export default App;
