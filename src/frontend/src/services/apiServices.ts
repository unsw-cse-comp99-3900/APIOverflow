import { Api, NewApi} from "../types/apiTypes";

export const deleteApi = async (api:Api) => {
    const res = await fetch(`/api/jobs/${api.id}`, {
      method: 'DELETE',
    });
    return;
};

const addApi = async (newApi: NewApi) => {
  const res = await fetch('/api/jobs', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(newApi),
  });

  return res;
};

const updateApi = async (api:Api) => {
    const res = await fetch(`/api/jobs/${api.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(api),
    });
    return;
  };