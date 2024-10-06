import { useState, useEffect } from 'react';
import {Api} from '../types/apiTypes';
import ApiListing from './ApiListing';
import Spinner from './Spinner';

const ApiListings = ({ isHome = false }) => {

  const [apis, setApis] = useState<Api[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchApis = async () => {
      const baseUrl = process.env.REACT_APP_API_BASE_URL;
      const apiUrl = isHome
        ? `${baseUrl}/apis?_limit=3`
        : `${baseUrl}/apis`;
      try {
        const res = await fetch(apiUrl);
        const data = await res.json();
        setApis(data);
      } catch (error) {
        console.log('Error fetching data', error);
      } finally {
        setLoading(false);
      }
    };

    fetchApis();
  }, [isHome]);

  return (
    <section className='bg-blue-50 px-4 py-10'>
      <div className='container-xl lg:container m-auto'>
        <h2 className='text-3xl font-bold text-indigo-500 mb-6 text-center'>
          {isHome ? 'Trending APIs' : 'Browse APIs'}
        </h2>
      
        {loading ? (
          <Spinner loading={loading} />
        ) : (
          <div className='grid grid-cols-[repeat(auto-fit,minmax(700px,1fr))] gap-6'>
          {apis.map((api) => (
            <ApiListing key={api.id} api={api} />
          ))}
          </div>
        )}
      </div>
    </section>
  );
  
};
export default ApiListings;
