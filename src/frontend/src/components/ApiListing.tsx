import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Api } from '../types/apiTypes';
import { FaPen, FaTrash } from 'react-icons/fa';
import Tag from './Tag';
import { deleteApi } from '../services/apiServices';
import { toast } from 'react-toastify';

const ApiListing = ({
  api,
  isMyApis,
  onDelete,
}: {
  api: Api;
  isMyApis: boolean;
  onDelete: (id: number) => void;
}) => {
  const [showFullDescription, setShowFullDescription] = useState(false);

  let description = api.description;

  if (!showFullDescription) {
    description = description.substring(0, 90) + '...';
  }

  const onDeleteClick = async (api: Api) => {
    const confirm = window.confirm('Are you sure you want to delete this listing?');
    if (!confirm) return;

    try {
      await deleteApi(api);
      toast.success('API deleted successfully');
      onDelete(api.id); // Trigger the deletion callback to update the state
    } catch (error) {
      toast.error('Failed to delete API');
    }
  };

  return (
    <div className='bg-white rounded-xl shadow-md relative'>
      <div className='p-4'>
        <div className='pb-16'>
          <div className='flex items-start mb-2'>
            <img
              src={api.icon_url}
              alt='API Icon'
              className='w-20 h-20 ml-4 mr-4 mt-2 rounded-full object-cover'
            />

            <div>
              <h3 className='text-xl font-bold my-2'>{api.name}</h3>
              <div className='text-gray-600'>{api.owner}</div>
              <div className='flex flex-wrap mt-4 mb-5'>
                {api?.tags?.map((tag, index) => (
                  <Tag key={index} tag={tag} className='mr-3 mb-2' />
                ))}
              </div>
            </div>
          </div>

          <div className='border border-gray-100 mb-5'></div>

          <div className='mb-5 break-words text-gray-700'>{description}</div>

          <button
            onClick={() => setShowFullDescription((prevState) => !prevState)}
            className='text-indigo-500 hover:text-indigo-600'
          >
            {showFullDescription ? 'Less' : 'More'}
          </button>
        </div>

        {isMyApis && (
          <div className='absolute top-8 right-8 flex space-x-2'>
            <Link
              to={`/add-api`}
              className='bg-white text-blue-800 hover:bg-blue-800 hover:text-white font-semibold px-3 py-3 rounded-lg'
            >
              <FaPen />
            </Link>
            <button
              className='bg-white text-red-500 hover:bg-red-500 hover:text-white font-semibold px-3 py-3 rounded-lg'
              onClick={() => onDeleteClick(api)}
            >
              <FaTrash />
            </button>
          </div>
        )}

        <div className='absolute bottom-8 right-8'>
          <Link
            to={`/apis/${api.id}`}
            className='h-[36px] bg-blue-800 hover:bg-amber-200 text-white hover:text-black font-semibold hover:underline px-4 py-2 rounded-lg text-center text-sm'
          >
            Read More
          </Link>
        </div>
      </div>
    </div>
  );
};

export default ApiListing;
