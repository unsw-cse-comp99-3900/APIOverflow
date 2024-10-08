import React from 'react';
import Spinner from './Spinner'; 
interface FetchStatusProps {
  loading: boolean;
  error: string | null;
  data: any;
  children: React.ReactNode;
}

const FetchStatus: React.FC<FetchStatusProps> = ({ loading, error, data, children }) => {
  if (loading) {
    return <Spinner loading={loading} />;
  }

  if (error) {
    return <div className="container m-auto py-6 px-6 text-red-500">{error}</div>;
  }

  if (!data) {
    return <div className="container m-auto py-6 px-6">No data found.</div>;
  }

  return <>{children}</>;
};

export default FetchStatus;
