import { LoginModel, ServicePost, ServiceUpdate, TagData, UserCreate } from "../types/backendTypes";
import { Tag } from "../types/miscTypes";
import { briefApiDataFormatter, detailedApiDataFormatter } from "../utils/dataFormatters";

let baseUrl = process.env.REACT_APP_API_BASE_URL;

/*        API Services        */
export const getApis = async (tags?: Tag[]) => {
  const queryParams = tags && tags.length > 0 ? `?tags=${tags.join(",")}` : "";
  const res = await fetch(`${baseUrl}/service/filter${queryParams}`, {
    method: "GET",
  });
  const data = await res.json();
  return data.map(briefApiDataFormatter);
};

export const getMyApis = async () => {
  const res = await fetch(`${baseUrl}/service/my_services`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
    method: "GET",
  });
  const data = await res.json();
  return data;
};

export const getApi = async (id: number | string) => {
  const res = await fetch(`${baseUrl}/service/get_service?sid=${id}`, {
    method: "GET",
  });
  const data = await res.json();
  return detailedApiDataFormatter(data);
};

export const deleteApi = async (id: string) => {
  await fetch(`${baseUrl}/service/delete?sid=${id}`, {
    method: "DELETE",
  });
  return;
};

export const addApi = async (service: ServicePost) => {
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

export const updateApi = async (api: ServiceUpdate) => {
  await fetch(`${baseUrl}/service/update`, {
    method: "PUT",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
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


/*        Tag Services       */
export const getTags = async () => {
  const res = await fetch(`${baseUrl}/tags/get`, {
    method: "GET",
  });
  const data = await res.json();
  return data.tags;
};

export const addTag = async (tag: TagData) => {
  await fetch(`${baseUrl}/tag/add`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(tag),
  });
  return;
};