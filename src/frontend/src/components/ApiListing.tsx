import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Api } from '../types/apiTypes';

const ApiListing = ({ api }: { api: Api }) => {
  const [showFullDescription, setShowFullDescription] = useState(false);

  let description = api.description;

  if (!showFullDescription) {
    description = description.substring(0, 90) + '...';
  }

  return (
    <div className='bg-white rounded-xl shadow-md relative'>
      <div className='p-4'>
        {/* Container for icon and owner + name */}
        <div className='flex items-start mb-6'>
          {/* Icon on the left */}
          <img
            src={api.icon_url}
            alt='API Icon'
            className='w-16 h-16 mr-4 mt-2 rounded-full object-cover'
          />

          {/* Content for owner and name */}
          <div>
            {/* Owner */}
            <div className='text-gray-600 my-2'>{api.owner}</div>

            {/* Name */}
            <h3 className='text-xl font-bold'>{api.name}</h3>
          </div>
        </div>
        <div className='border border-gray-100 mb-5'></div>

        {/* Description (without icon) */}
        <div className='mb-5 break-words text-gray-700'>{description}</div>

        <button
          onClick={() => setShowFullDescription((prevState) => !prevState)}
          className='text-indigo-500 mb-5 hover:text-indigo-600'
        >
          {showFullDescription ? 'Less' : 'More'}
        </button>

        <div className='flex flex-col lg:flex-row justify-between mb-4'>
          <div className='ml-auto'>
            <Link
              to={`/apis/${api.id}`}
              className='h-[36px] bg-indigo-500 hover:bg-indigo-600 text-white px-4 py-2 rounded-lg text-center text-sm'
            >
              Read More
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ApiListing;
