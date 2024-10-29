import { json } from "stream/consumers";
import {
  LoginModel,
  ServiceIconInfo,
  ServicePost,
  ServiceReviewInfo,
  ServiceUpdate,
  ServiceUpload,
  TagData,
  UserCreate,
} from "../types/backendTypes";
import { Tag } from "../types/miscTypes";
import {
  briefApiDataFormatter,
  detailedApiDataFormatter,
} from "../utils/dataFormatters";

let baseUrl = process.env.REACT_APP_API_BASE_URL;

/*        API Services        */
export const getApis = async (tags?: Tag[], hidePending : boolean = false) => {
  const queryParams =
    tags && tags.length > 0 ? `&tags=${tags.join("&tags=")}` : "";
  const response = await fetch(`${baseUrl}/service/filter?hide_pending=${hidePending}${queryParams}`, {
    method: "GET",
  });
  const data = await response.json();
  console.log(data)
  return data.map(briefApiDataFormatter);
};

export const getMyApis = async () => {
  const response = await fetch(`${baseUrl}/service/my_services`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
    method: "GET",
  });

  if (response.status === 401) {
    throw new Error("Unauthorized");
  }

  const data = await response.json();
  return data;
};

export const getApi = async (id: string) => {
  const response = await fetch(`${baseUrl}/service/get_service?sid=${id}`, {
    method: "GET",
  });
  const data = await response.json();
  if (response.status === 404) {
    throw new Error("Service Not Found");
  }
  console.log(data)
  return detailedApiDataFormatter(data);
};

export const deleteApi = async (id: string) => {
  await fetch(`${baseUrl}/service/delete?sid=${id}`, {
    method: "DELETE",
  });
  return;
};

export const addApi = async (service: ServicePost) => {
  const response = await fetch(`${baseUrl}/service/add`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(service),
  });

  if (response.status === 401) {
    throw new Error("Unauthorized");
  }

  const data = await response.json();
  return data.id;
};

export const updateApi = async (api: ServiceUpdate) => {
  const response = await fetch(`${baseUrl}/service/update`, {
    method: "PUT",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(api),
  });

  if (response.status === 401) {
    throw new Error("Unauthorized");
  }
  return;
};

/*        Auth Services       */
export const userLogin = async (credentials: LoginModel) => {
  const response = await fetch(`${baseUrl}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(credentials),
  });

  if (!response.ok) {
    const errorDetails = await response.text();
    console.error("Error:", errorDetails);
    throw new Error(`Request failed with status ${response.status}`);
  }

  const data = await response.json();
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
  const response = await fetch(`${baseUrl}/tags/get`, {
    method: "GET",
  });
  const data = await response.json();
  return data.tags;
};

export const addTag = async (tag: TagData) => {
  const response = await fetch(`${baseUrl}/tag/add`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(tag),
  });

  if (response.status === 401) {
    throw new Error("Unauthorized");
  }
  return;
};

/*        Image Services       */

// Upload image to database
export const uploadImage = async (file: File) => {
  const formData = new FormData();
  formData.append("file", file);
  const response = await fetch(`${baseUrl}/upload/imgs`, {
    method: "POST",
    body: formData,
  });
  const data = await response.json();
  console.log(data)
  return data.doc_id;
};

// Link icon with service
export const apiAddIcon = async (info: ServiceIconInfo) => {
  const response = await fetch(`${baseUrl}/service/add_icon`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(info),
  });
};

export const apiGetIcon = async (sid: string) => {
  console.log(sid)
  const response = await fetch(`${baseUrl}/service/get/icon?sid=${sid}`, {
    headers: {
      "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
      Pragma: "no-cache",
      Expires: "0",
    },
    method: "GET",
  });
  const blob = await response.blob(); // Get the Blob data
  const url = URL.createObjectURL(blob); // Create a URL for the Blob
  if(blob.size === 62114){
    console.log(`icon for sid ${sid}: lmao`)
  }else if (blob.size === 29457){
    console.log(`icon for sid ${sid}: flooshed`)
  }else if (blob.size === 8255){
    console.log(`icon for sid ${sid}: default`)
  }else{
    console.log("icon: WTF IS HAPPENING")
  }
  console.log(blob.size)
  return url
};

/*        Document Services       */

// Upload service to database
export const uploadPDF = async (file: File) => {
  const formData = new FormData();
  formData.append("file", file);
  const response = await fetch(`${baseUrl}/upload/pdfs`, {
    method: "POST",
    body: formData,
  });
  const data = await response.json();
  return data.doc_id;
}

// Link service with documentation
export const uploadDocs = async (info: ServiceUpload) => {
  const response = await fetch(`${baseUrl}/service/upload_docs`, {
    method: "POST",
    headers: {  
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(info),
  });
}

export const getDoc = async (doc_id: string) => {
  const response = await fetch(`${baseUrl}/get/doc?doc_id=${doc_id}`, {
    method: "GET",
  });
  const blob = await response.blob(); // Get the Blob data
  const url = URL.createObjectURL(blob); // Create a URL for the Blob
  return url
}

/*        Review Services       */
export const apiAddReview = async (info: ServiceReviewInfo) => {
  const response = await fetch(`${baseUrl}/service/review/add`, {
    method: "POST",
    headers: {  
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
    },
    
    body: JSON.stringify(info),
  });
  const data = await response.json();
  if (response.status === 403) {
    throw new Error(data.detail);
  }
}

export const apiGetReviews = async (sid: string, testing:boolean=true) => {
  const response = await fetch(`${baseUrl}/service/get/reviews?sid=${sid}&testing=${testing}`, {
    method: "GET",
  });
  const data = await response.json();
  return data.reviews;
}