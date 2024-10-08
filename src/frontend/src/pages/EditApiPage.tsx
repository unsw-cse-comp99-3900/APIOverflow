import React from "react";
import EditApiForm from "../components/UpdateApiForm";
import { useParams } from "react-router-dom";

const EditApiPage = () => {
  const { id } = useParams();
  const numericApiId = Number(id);
  
  return (
    <section className="w-full h-full relative bg-gradient-to-b from-blue-50 to-white px-6">
      <EditApiForm apiId={numericApiId} />
    </section>
  );
};

export default EditApiPage;
