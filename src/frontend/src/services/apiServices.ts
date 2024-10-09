import { Api, DetailedApi, NewApi } from "../types/apiTypes";
import { LoginModel, ServicePost, UserCreate } from "../types/backendTypes";
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
  const res = await fetch(`${baseUrl}/service/my_services`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
    method: "GET",
  });
  const data = await res.json();
  return removeUnderscores(data);
};

export const getApi = async (id: number | string) => {
  const res = await fetch(`${baseUrl}/service/get_service?sid=${id}`, {
    method: "GET",
  });
  const data = await res.json();
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

export const addApi = async (service: ServicePost) => {
  console.log(service)
  const res = await fetch(`${baseUrl}/service/add`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(service),
  });
  const data = await res.json();
  return data.id;
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
export const userLogin = async (credentials: LoginModel) => {
  const res = await fetch(`${baseUrl}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(credentials),
  });

  if (!res.ok) {
    const errorDetails = await res.text();
    console.error("Error:", errorDetails);
    throw new Error(`Request failed with status ${res.status}`);
  }

  const data = await res.json();
  return data.access_token;
};

export const userRegister = async (user: UserCreate) => {
  await fetch(`${baseUrl}/auth/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(user),
  });
  return;
};
