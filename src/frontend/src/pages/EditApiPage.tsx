import React from "react";
import EditApiForm from "../components/EditApiForm";
import { useParams } from "react-router-dom";
import UpdateApiForm from "../components/UpdateApiForm";

const EditApiPage: React.FC = () => {
  const { id } = useParams();
  
  return (
      <EditApiForm apiId={id} />
  );
};

export default EditApiPage;
