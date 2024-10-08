import { Api, NewApi} from "../types/apiTypes";

let baseUrl = process.env.REACT_APP_API_BASE_URL

export const getApis = async () => {
    const res = await fetch(`${baseUrl}/apis`);
    const data = await res.json();
    return data;
}

export const getMyApis = async () => {
  const res = await fetch(`${baseUrl}/apis`);
  const data = await res.json();
  return data;
}

export const getApi = async (id:number) => {
  const res = await fetch(`${baseUrl}/apis/${id}`);
  const data = await res.json();
  return data;
}

export const deleteApi = async (apiId:number) => {
    const res = await fetch(`${baseUrl}/apis/${apiId}`, {
      method: 'DELETE',
    });
    return;
};

const addApi = async (newApi: NewApi) => {
  const res = await fetch(`${baseUrl}/apis`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(newApi),
  });

  return res;
};

const updateApi = async (api:Api) => {
    const res = await fetch(`${baseUrl}/apis/${api.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(api),
    });
    return;
  };