import React from "react";
import ApiListings from "../components/ApiListings";

const MyApisPage: React.FC = () => {
  return (
      <ApiListings isMyAPis={true} selectedTags={[]}/>
  );
};

export default MyApisPage;
