// loaders.ts
import { LoaderFunctionArgs } from 'react-router-dom';
import { Api } from '../types/apiTypes';  // Importing Job type

export const apiLoader = async ({ params }: LoaderFunctionArgs): Promise<Api> => {
  const res = await fetch(`/api/jobs/${params.id}`);

  if (!res.ok) {
    throw new Error('Failed to fetch job data');
  }

  const data: Api = await res.json();
  return data;
};
