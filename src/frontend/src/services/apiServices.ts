import { Api, DetailedApi, NewApi } from "../types/apiTypes";
import { apiDataFormatter } from "../utils/dataFormatters";
import { removeUnderscores } from "../utils/removeUnderscores";

let baseUrl = process.env.REACT_APP_API_BASE_URL;

/*        API Services        */
export const getApis = async () => {
  const res = await fetch(`${baseUrl}/service/apis`, {
    method: "GET",
  });
  const data = await res.json();
  return removeUnderscores(data).map(apiDataFormatter);
};

export const getMyApis = async () => {
  console.log({
    headers:{
      Authorization: `Bearer ${localStorage.getItem("token")}`
    },
    method: "GET",
  })
  const res = await fetch(`${baseUrl}/service/my_services`, {
    headers:{
      Authorization: `Bearer ${localStorage.getItem("token")}`
    },
    method: "GET",
  });
  const data = await res.json();
  return removeUnderscores(data);
};

export const getApi = async (id: number) => {
  const res = await fetch(`${baseUrl}/service/get_service?id=${id}`, {
    method: "GET",
  });
  const data = await res.json();
  console.log(data);
  return apiDataFormatter(removeUnderscores(data));
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

/*        Auth Services       */
export const userLogin = async (username: string, password: string) => {
  const res = await fetch(`${baseUrl}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ 
      username, 
      password 
    }), 
  });

  if (!res.ok) {
    const errorDetails = await res.text();
    console.error("Error:", errorDetails);
    throw new Error(`Request failed with status ${res.status}`);
  }

  const data = await res.json();
  return data.access_token;
};
