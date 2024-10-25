import React from "react";
import EditApiForm from "../components/UpdateApiForm";
import { useParams } from "react-router-dom";

const EditApiPage = () => {
  const { id } = useParams();
  
  return (
      <EditApiForm apiId={id} />
  );
};

export default EditApiPage;
