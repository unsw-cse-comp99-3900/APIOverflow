import { Api, NewApi } from "../types/apiTypes";
import { removeUnderscores } from "../utils/removeUnderscores";

let baseUrl = process.env.REACT_APP_API_BASE_URL;

export const getApis = async () => {
  const res = await fetch(`${baseUrl}/service/apis`, {
    method: "GET",
  });
  const data = await res.json();
  return removeUnderscores(data);
};

export const getMyApis = async () => {
  const res = await fetch(`${baseUrl}/service/my_services`, {
    method: "GET",
  });
  const data = await res.json();
  return removeUnderscores(data);
};

export const getApi = async (id: number) => {
  const res = await fetch(`${baseUrl}/service`, {
    method: "GET",
    body: JSON.stringify(id),
  });
  const data = await res.json();
  return removeUnderscores(data);
};

// BE un-implemented
export const deleteApi = async (id: number) => {
    await fetch(`${baseUrl}/service/${id}`, {
    method: "DELETE",
    body: JSON.stringify(id),
  });
  return;
};

export const addApi = async (newApi: NewApi) => {
  const res = await fetch(`${baseUrl}/service/add`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(newApi),
  });
  return res;
};

// BE un-implemented
export const updateApi = async (api: Api) => {
    await fetch(`${baseUrl}/service/${api.id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(api),
  });
  return;
};
