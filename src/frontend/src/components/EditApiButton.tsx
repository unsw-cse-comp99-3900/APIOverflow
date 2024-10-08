import React from "react";
import { Link } from "react-router-dom";
import { FaPen } from "react-icons/fa";
import { Api } from "../types/apiTypes";

const EditApiButton = () => {
  return (
    <Link
      to={`/add-api`}
      className="bg-white text-blue-800 hover:bg-blue-800 hover:text-white font-semibold px-3 py-3 rounded-lg"
    >
      <FaPen />
    </Link>
  );
};

export default EditApiButton;
