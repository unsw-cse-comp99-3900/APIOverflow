import React from "react";
import { FaArrowLeft } from "react-icons/fa";
import { Link } from "react-router-dom";

interface BackButtonProps {
  toUrl: string;
}

const BackButton: React.FC<BackButtonProps> = ({ toUrl }) => {
  return (
    <div className="container m-auto pt-6 px-6">
      <Link
        to={toUrl}
        className="text-blue-800 hover:text-indigo-500 hover:underline font-bold flex items-center"
      >
        <FaArrowLeft className="mr-2" /> Back
      </Link>
    </div>
  );
};

export default BackButton;
