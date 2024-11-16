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
import MyApisPage from "./pages/MyApisPage";
import MyApiPage from "./pages/MyApiPage";
import ThemeLayout from "./layouts/ThemeLayout";
import { AuthProvider } from "./contexts/AuthContext";
import RegisterPage from "./pages/RegisterPage";
import LoginPage from "./pages/LoginPage";
import TagsSidebarLayout from "./layouts/TagsSidebarLayout";
import UserSidebarLayout from "./layouts/UserSidebarLayout";
import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "./contexts/AuthContext";
import NotFoundPage from "./pages/NotFoundPage";
import ReviewManagement from "./pages/ReviewManagement";
import ServiceManagement from "./pages/ServiceManagement";
import UserManagement from "./pages/UserManagement";

const ProtectedRoute = () => {
  const auth = useAuth();
  const { isLoggedIn } = auth!;

  if (!isLoggedIn) {
    return <Navigate to="/login" replace />;
  }
  return <Outlet />;
};

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
          <Route path="/apis/:id" element={<ApiPage />} />
          <Route path="/add-api" element={<AddApiPage />} />
          <Route path="/edit-api" element={<EditApiPage />} />
          <Route path="/apis" element={<TagsSidebarLayout />}>
            <Route path="/apis" element={<APIsPage />} />
          </Route>
          
          <Route element={<ProtectedRoute />}>
            <Route path="/admin/reviews" element={<ReviewManagement />} />
            <Route path="/admin/services" element={<ServiceManagement />} />
            <Route path="/admin/users" element={<UserManagement />} />
            <Route path="/profile" element={<UserSidebarLayout />}>
              <Route path="/profile/my-apis" element={<MyApisPage />} />
              <Route path="/profile/my-apis/:id" element={<MyApiPage />} />
              <Route path="/profile/add-api" element={<AddApiPage />} />
              <Route
                path="/profile/my-apis/:id/edit"
                element={<EditApiPage />}
              />
            </Route>
          </Route>
          <Route path="/*" element={<NotFoundPage />} />
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
