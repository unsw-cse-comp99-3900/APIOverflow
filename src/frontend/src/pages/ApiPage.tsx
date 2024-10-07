import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { FaArrowLeft } from 'react-icons/fa';
import { toast } from 'react-toastify';
import { Api } from '../types/apiTypes';
import { getApi } from '../services/apiServices';
import FetchStatus from '../components/FetchStatus';  // Import the new reusable component
import Tag from '../components/Tag';

const ApiPage = () => {
  const [api, setApi] = useState<Api | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { id } = useParams();

  useEffect(() => {
    const fetchApi = async () => {
      try {
        const data = await getApi(Number(id));
        setApi(data);
      } catch (error) {
        console.log('Error fetching data', error);
        setError('Failed to load API data');
        toast.error('Error loading API data');
      } finally {
        setLoading(false);
      }
    };

    fetchApi();
  }, [id]); // Ensure the effect runs whenever the id changes

  return (
    <>
      {/* Main Layout */}
      <section className="w-full h-full relative bg-gradient-to-b from-blue-50 to-white py-10 px-6">
      <div className="container m-auto py-6 px-6">
          <Link to="/apis" className="text-blue-800 hover:text-indigo-500 hover:underline font-bold flex items-center">
            <FaArrowLeft className="mr-2" /> Back to Api Listings
          </Link>
        </div>
        <FetchStatus loading={loading} error={error} data={api}>
          {/* Header Section */}
          <div className="mx-auto max-w-[100rem] relative bg-white rounded-2xl shadow-lg p-10">
            <div className="flex items-center">

              {/* Placeholder for API icon */}
              <div className="flex flex-shrink-0 items-center">  {/* Adjust pl-10 as needed for custom padding */}
                <img
                  className='w-56 h-56 rounded-full object-cover mx-auto'
                  src={api?.icon_url}
                  alt="API Icon"
                />
              </div>

              {/* Parent div */}
              <div className="ml-10 w-full">  
                {/* Fixed top margin for API Name */}
                <h1 className="text-4xl font-bold mb-5">{api?.name}</h1>
                
                {/* Gray border that spans full width */}
                <div className="border border-gray-100 w-full mb-5"></div>

                {/* Tags section */}
                <div className="flex flex-wrap max-w-3xl mt-4 mb-5">
                  {api?.tags.map((tag, index) => (
                    <Tag key={index} tag={tag} className="mr-3 mb-2" />
                  ))}
                </div>
              </div>


            </div>
          </div>

          {/* Reviews, Description, Documentation */}
          <div className="flex mx-auto max-w-[100rem] mt-10 space-x-10">
            <div className="w-1/4 bg-white rounded-2xl shadow-lg p-6">
              <h2 className="text-xl font-bold mb-4">Reviews</h2>
              {/* Placeholder for Reviews */}
              <p>No reviews yet</p>
            </div>
            <div className="w-1/2 bg-white rounded-2xl shadow-lg p-6">
              <h2 className="text-xl font-bold mb-4">Description</h2>
              {/* API Description */}
              <p className="break-words">{api?.description}</p>
            </div>
            <div className="w-1/4 bg-white rounded-2xl shadow-lg p-6">
              <h2 className="text-xl font-bold mb-4">Documentation</h2>
              {/* Placeholder for Documentation */}
              <p>Coming soon</p>
            </div>
          </div>
        </FetchStatus>
      </section>
    </>
  );
};

export default ApiPage;
