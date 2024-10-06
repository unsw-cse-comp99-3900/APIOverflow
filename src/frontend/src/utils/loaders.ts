// loaders.ts
import { LoaderFunctionArgs } from 'react-router-dom';
import { Api } from '../types/apiTypes';  // Importing Job type

export const apiLoader = async ({ params }: LoaderFunctionArgs): Promise<Api> => {
    let baseUrl = process.env.REACT_APP_API_BASE_URL
    const res = await fetch(`${baseUrl}/apis/${params.id}`);
  if (!res.ok) {
    throw new Error('Failed to fetch job data');
  }
  const data: Api = await res.json();
  console.log(data)
  return data;
};
