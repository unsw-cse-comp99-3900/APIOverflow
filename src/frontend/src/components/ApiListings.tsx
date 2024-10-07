import { useState, useEffect } from 'react';
import { Api } from '../types/apiTypes';
import ApiListing from './ApiListing';
import Spinner from './Spinner';
import { getApis } from '../services/apiServices';

const ApiListings = ({ isMyAPis }: { isMyAPis: boolean }) => {
  const [apis, setApis] = useState<Api[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchApis = async () => {
      try {
        const data = await getApis();
        setApis(data);
      } catch (error) {
        console.log('Error fetching data', error);
      } finally {
        setLoading(false);
      }
    };

    fetchApis();
  }, []);

  const handleDelete = (deletedApiId: number) => {
    setApis((prevApis) => prevApis.filter((api) => api.id !== deletedApiId));
  };

  return (
    <section className='bg-gradient-to-b from-blue-50 to-white px-4 py-10'>
      <div className='container-xl lg:container m-auto'>
        <h2 className='text-3xl font-bold text-blue-800 mb-6 text-center'>
          {isMyAPis ? 'My APIs' : 'Browse APIs'}
        </h2>

        {loading ? (
          <Spinner loading={loading} />
        ) : (
          <div className='grid grid-cols-[repeat(auto-fit,minmax(700px,1fr))] gap-6'>
            {apis.map((api) => (
              <ApiListing
                key={api.id}
                api={api}
                isMyApis={isMyAPis}
                onDelete={handleDelete}
              />
            ))}
          </div>
        )}
      </div>
    </section>
  );
};

export default ApiListings;
