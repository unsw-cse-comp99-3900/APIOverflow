import React from "react";
import ApiListings from "../components/ApiListings";

const MyApisPage = () => {
  return (
    <section className='bg-gradient-to-b from-blue-50 to-white py-6'>
      <ApiListings isMyAPis={true} />
    </section>
  );
};

export default MyApisPage;
