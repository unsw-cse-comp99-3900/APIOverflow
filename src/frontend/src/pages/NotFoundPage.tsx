import React from "react";
import NotFound from "../assets/images/404.gif";

const NotFoundPage: React.FC = () => {
  return (
    <>
      <div className="flex flex-col items-center justify-center w-full h-full py-24 bg-white">
        <img
          src={NotFound}
          alt="404 Not Found"
        />

      </div>
      <div className="flex flex-col items-center mt-10">
        <h1 className="text-4xl font-bold text-blue-800 text-center">
          Oops, cannot find what you are looking for :(
        </h1>
      </div>
    </>
  );
};

export default NotFoundPage;
