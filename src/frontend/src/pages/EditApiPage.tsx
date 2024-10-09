import React from "react";
import EditApiForm from "../components/UpdateApiForm";
import { useParams } from "react-router-dom";

const EditApiPage = () => {
  const { id } = useParams();
  const numericApiId = Number(id);
  
  return (
      <EditApiForm apiId={numericApiId} />
  );
};

export default EditApiPage;
