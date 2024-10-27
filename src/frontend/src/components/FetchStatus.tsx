import React, { useEffect } from "react";
import Spinner from "./Spinner";
import { useNavigate } from "react-router-dom";

interface FetchStatusProps {
  loading: boolean;
  error: string | null;
  data: any;
  children: React.ReactNode;
}

const FetchStatus: React.FC<FetchStatusProps> = ({
  loading,
  error,
  data,
  children,
}) => {
  const navigate = useNavigate();

  useEffect(() => {
    if (error === "Unauthorized") {
      localStorage.removeItem("token");
      navigate("/login");
    } else if (error === "Service Not Found") {
      navigate("/NotFound");
    }
  }, [error, navigate]);
  if (loading) {
    return <Spinner loading={loading} />;
  }

  if (error && error !== "Unauthorized") {
    return (
      <div className="container m-auto py-6 px-6 text-red-500">{error}</div>
    );
  }

  if (!data) {
    return <div className="container m-auto py-6 px-6">No data found.</div>;
  }

  return <>{children}</>;
};

export default FetchStatus;
