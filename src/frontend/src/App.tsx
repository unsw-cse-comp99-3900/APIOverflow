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
import MyProfilePage from "./pages/UserProfilePage";
import PasswordResetRequest from './components/PasswordResetRequest';
import PasswordReset from './components/PasswordReset';

import VerificationPage from "./pages/VerificationPage";
import MyReviewsPage from "./pages/MyReviewsPage";
import MyRepliesPage from "./pages/MyRepliesPage";

const UserProtectedRoute = () => {
  const auth = useAuth();
  const { isLoggedIn } = auth!;

  if (!isLoggedIn) {
    return <Navigate to="/login" replace />;
  }
  return <Outlet />;
};

const AdminProtectedRoute = () => {
  const auth = useAuth();
  const { isAdmin } = auth!;

  if (!isAdmin) {
    return <Navigate to="/profile/my-profile" replace />;
  }
  return <Outlet />;
};

const SuperAdminProtectedRoute = () => {
  const auth = useAuth();
  const { isSuperAdmin } = auth!;

  if (!isSuperAdmin) {
    return <Navigate to="/profile/my-profile" replace />;
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
          <Route path="/verify-email" element={<VerificationPage />}/>
        </Route>

        <Route path="/" element={<ContentLayout />}>
          <Route path="/apis/:id" element={<ApiPage />} />
          <Route path="/add-api" element={<AddApiPage />} />
          <Route path="/edit-api" element={<EditApiPage />} />
          <Route path="/apis" element={<TagsSidebarLayout />}>
            <Route path="/apis" element={<APIsPage />} />
          </Route>
          <Route path="/forgot-password" element={<PasswordResetRequest />} />
          <Route path="/reset-password/:token" element={<PasswordReset />} />
          <Route path="/verified-password-reset" element={<PasswordReset />} />
          <Route element={<UserProtectedRoute />}>
            <Route path="/profile" element={<UserSidebarLayout />}>
              <Route element={<AdminProtectedRoute />}>
                <Route path="/profile/admin/services" element={<ServiceManagement />} />
                <Route element={<SuperAdminProtectedRoute />}>
                  <Route path="/profile/admin/users" element={<UserManagement />} />
                </Route>
              </Route>
              <Route path="/profile/my-profile" element={<MyProfilePage />} />
              <Route path="/profile/my-apis" element={<MyApisPage />} />
              <Route path="/profile/my-apis/:id" element={<MyApiPage />} />
              <Route path="/profile/add-api" element={<AddApiPage />} />
              <Route path="/profile/my-apis/:id/edit" element={<EditApiPage />}/>
              <Route path="/profile/my-reviews" element={<MyReviewsPage/>}/>
              <Route path="/profile/my-replies" element={<MyRepliesPage/>}/>
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
