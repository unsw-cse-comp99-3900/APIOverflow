import {
  Route,
  createBrowserRouter,
  createRoutesFromElements,
  RouterProvider,
} from "react-router-dom";
import ContentLayout from "./layouts/ContentLayout";
import HomePage from "./pages/HomePage";
import APIsPage from "./pages/ApisPage";
import AddApiPage from "./pages/AddApiPage";
import ApiPage from "./pages/ApiPage";
import EditApiPage from "./pages/EditApiPage";
import UserProfileLayout from "./layouts/UserProfileLayout";
import MyApisPage from "./pages/MyApisPage";
import MyApiPage from "./pages/MyApiPage";
import ThemeLayout from "./layouts/ThemeLayout";
import { AuthProvider } from "./authentication/AuthProvider";
import RegisterPage from "./pages/RegisterPage";
import LoginPage from "./pages/LoginPage";
import ProtectedRoute from "./authentication/ProtectedRoute";

const App = () => {
  const router = createBrowserRouter(
    createRoutesFromElements(
      <>
        <Route path="/" element={<ThemeLayout />}>
          <Route index element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
        </Route>

        <Route path="/" element={<ContentLayout />}>
          <Route path="/apis" element={<APIsPage />} />
          <Route path="/apis/:id" element={<ApiPage />} />
          <Route path="/add-api" element={<AddApiPage />} />
          <Route path="/edit-api" element={<EditApiPage />} />

          <Route path="/apis" element={<APIsPage />} />
          <Route element={<ProtectedRoute />}>
            <Route path="/profile" element={<UserProfileLayout />}>
              <Route path="/profile/my-apis" element={<MyApisPage />} />
              <Route path="/profile/my-apis/:id" element={<MyApiPage />} />
              <Route path="/profile/add-api" element={<AddApiPage />} />
              <Route
                path="/profile/my-apis/:id/edit"
                element={<EditApiPage />}
              />
            </Route>
          </Route>
        </Route>
      </>
    )
  );

  return (
    <AuthProvider>
      <RouterProvider router={router} />
    </AuthProvider>
  );
};

export default App;
