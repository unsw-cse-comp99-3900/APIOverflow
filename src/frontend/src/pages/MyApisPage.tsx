import React from 'react';
import ApiListings from '../components/ApiListings';

const MyApisPage = () => {
  return (
    <section>
      <ApiListings isMyAPis={true} />
    </section>
  );
};

export default MyApisPage;
