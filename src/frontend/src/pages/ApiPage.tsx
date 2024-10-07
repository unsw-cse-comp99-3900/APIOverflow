import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { FaArrowLeft } from 'react-icons/fa';
import { toast } from 'react-toastify';
import { Api } from '../types/apiTypes';
import { DeleteApiService } from '../types/apiServiceTypes';
import { getApi } from '../services/apiServices';
import FetchStatus from '../components/FetchStatus';  // Import the new reusable component

const ApiPage = ({ deleteApi }: DeleteApiService) => {
  const navigate = useNavigate();
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

  const onDeleteClick = (api: Api) => {
    const confirm = window.confirm('Are you sure you want to delete this listing?');
    if (!confirm) return;

    deleteApi(api);
    toast.success('API deleted successfully');
    navigate('/apis');
  };

  return (
    <>
      <section>
        <div className="container m-auto py-6 px-6">
          <Link to="/apis" className="text-indigo-500 hover:text-indigo-600 flex items-center">
            <FaArrowLeft className="mr-2" /> Back to Api Listings
          </Link>
        </div>
      </section>

      <section className="bg-indigo-50">
        <div className="container m-auto py-10 px-6">
          <FetchStatus loading={loading} error={error} data={api}>
            <div className="grid grid-cols-1 md:grid-cols-70/30 w-full gap-6">
              <main>
                <div className="bg-white p-6 rounded-lg shadow-md text-center md:text-left">
                  <div className="text-gray-500 mb-4">{api?.name}</div>
                  <h1 className="text-3xl font-bold mb-4">{api?.name}</h1>
                </div>

                <div className="bg-white p-6 rounded-lg shadow-md mt-6">
                  <h3 className="text-indigo-800 text-lg font-bold mb-6">Api Description</h3>
                  <p className="mb-4 break-words">{api?.description}</p>
                </div>
              </main>

              <aside className="w-full md:w-1/3 p-4">
                <div className="bg-white p-6 rounded-lg shadow-md mt-6">
                  <h3 className="text-xl font-bold mb-6">Manage Api</h3>
                  <Link
                    to={`/edit-api/${api?.id}`}
                    className="bg-indigo-500 hover:bg-indigo-600 text-white text-center font-bold py-2 px-4 rounded-full w-full focus:outline-none focus:shadow-outline mt-4 block"
                  >
                    Edit Api
                  </Link>
                  <button
                    onClick={() => onDeleteClick(api!)}  // Ensure api exists before deleting
                    className="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded-full w-full focus:outline-none focus:shadow-outline mt-4 block"
                  >
                    Delete Api
                  </button>
                </div>
              </aside>
            </div>
          </FetchStatus>
        </div>
      </section>
    </>
  );
};

export default ApiPage;
