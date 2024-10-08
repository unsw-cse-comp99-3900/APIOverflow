import { Api, NewApi } from "../types/apiTypes";

let baseUrl = process.env.REACT_APP_API_BASE_URL;

export const getApis = async () => {
  const res = await fetch(`${baseUrl}/apis`);
  const data = await res.json();
  return data;
};

export const getMyApis = async () => {
  const res = await fetch(`${baseUrl}/apis`);
  const data = await res.json();
  return data;
};

export const getApi = async (id: number) => {
  console.log(id);
  const res = await fetch(`${baseUrl}/apis/${id}`);
  const data = await res.json();
  return data;
};

export const deleteApi = async (id: number) => {
  await fetch(`${baseUrl}/apis/${id}`, {
    method: "DELETE",
  });
  return;
};

export const addApi = async (newApi: NewApi) => {
  const res = await fetch(`${baseUrl}/apis`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(newApi),
  });

  return res;
};

export const updateApi = async (api: Api) => {
  await fetch(`${baseUrl}/apis/${api.id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(api),
  });
  return;
};
