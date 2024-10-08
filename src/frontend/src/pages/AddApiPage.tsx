import React from "react";
import { PhotoIcon } from "@heroicons/react/24/solid";
import EditApiForm from "../components/EditApiForm";

const AddApiPage = () => {
  return (
    <section className="w-full h-full relative bg-gradient-to-b from-blue-50 to-white px-6">
      <EditApiForm />
    </section>
  );
};

export default AddApiPage;
