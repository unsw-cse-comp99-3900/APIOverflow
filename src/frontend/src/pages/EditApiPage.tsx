import React from "react";
import EditApiForm from "../components/UpdateApiForm";
import { useParams } from "react-router-dom";

const EditApiPage: React.FC = () => {
  const { id } = useParams();
  
  return (
      <EditApiForm apiId={id} />
  );
};

export default EditApiPage;
