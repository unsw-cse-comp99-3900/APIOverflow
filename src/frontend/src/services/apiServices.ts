import {
  Endpoint,
  LoginModel,
  EndpointParameter,
  ServiceIconInfo,
  ServiceAdd,
  ServiceReviewInfo,
  ServiceUpdate,
  ServiceUpload,
  TagData,
  UserCreate,
  EndpointResponse,
} from "../types/backendTypes";
import { Rating, Tag } from "../types/miscTypes";
import {
  briefApiDataFormatter,
  detailedApiDataFormatter,
} from "../utils/dataFormatters";

let baseUrl = process.env.REACT_APP_API_BASE_URL;

/*        API Services        */
export const getApis = async (tags?: Tag[], hidePending: boolean = false) => {
  const queryParams =
    tags && tags.length > 0 ? `&tags=${tags.join("&tags=")}` : "";
  const response = await fetch(
    `${baseUrl}/service/filter?hide_pending=${hidePending}${queryParams}`,
    {
      method: "GET",
    }
  );
  const data = await response.json();
  console.log(data);
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
  console.log(data);
  return detailedApiDataFormatter(data);
};

export const deleteApi = async (id: string) => {
  await fetch(`${baseUrl}/service/delete?sid=${id}`, {
    method: "DELETE",
  });
  return;
};

export const addApi = async (
  name: string,
  description: string,
  tags: string[],
  endpointLink: string,
) => {

  const ParameterPlaceholder : EndpointParameter = {
    id: "1",
    endpoint_link: endpointLink,
    required: false,
    type: "BODY",
    name: "Parameter Placeholder",
    value_type: "string",
    example: "Example Placeholder",
  }

  const ResponsePlaceholder : EndpointResponse = {
    code: "1",
    description: "Description Placeholder",
    conditions: ["Condition Placeholder"],
    example: "Example Placeholder",
  }

  const endpoint: Endpoint = {
    link: endpointLink,
    title_description: "Title Description Placeholder",
    main_description: "Main Description Placeholder",
    tab: "Tab Placeholder",
    parameters: [ParameterPlaceholder],
    method: "GET",
    responses: [ResponsePlaceholder]
  }

  const api: ServiceAdd = {
    name,
    description,
    endpoints: [endpoint],
    tags,
  };

  const response = await fetch(`${baseUrl}/service/add`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(api),
  });

  if (response.status === 401) {
    throw new Error("Unauthorized");
  }

  const data = await response.json();
  return data.id;
};

export const updateApi = async (
  name: string,
  description: string,
  tags: string[],
  endpoint: string,
  sid: string
) => {
  const api: ServiceUpdate = {
    sid,
    name,
    description,
    endpoint,
    tags: tags,
  };
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

export const userRegister = async (
  email: string,
  username: string,
  password: string,
  displayname: string

) => {
  const newUser: UserCreate = {
    email,
    username,
    password,
    displayname,
  };
  await fetch(`${baseUrl}/auth/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(newUser),
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

export const addTag = async (tagName: string) => {
  const tag: TagData = {
    tag: tagName,
  };
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
  return data.doc_id;
};

// Link icon with service
export const apiAddIcon = async (sid: string, docId: string) => {
  const info: ServiceIconInfo = {
    sid,
    doc_id: docId,
  };
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
  return url;
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
};

// Link service with documentation
export const uploadDocs = async (sid: string, docId: string) => {
  const info: ServiceUpload = {
    sid,
    doc_id: docId,
  };
  const response = await fetch(`${baseUrl}/service/upload_docs`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(info),
  });
};

export const getDoc = async (doc_id: string) => {
  const response = await fetch(`${baseUrl}/get/doc?doc_id=${doc_id}`, {
    method: "GET",
  });
  const blob = await response.blob(); // Get the Blob data
  const url = URL.createObjectURL(blob); // Create a URL for the Blob
  return url;
};

/*        Review Services       */
export const apiAddReview = async (
  sid: string,
  rating: Rating,
  title: string,
  comment: string
) => {
  const info: ServiceReviewInfo = {
    sid,
    rating,
    title,
    comment,
  };
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
};

export const apiGetReviews = async (sid: string, testing: boolean = true) => {
  const response = await fetch(
    `${baseUrl}/service/get/reviews?sid=${sid}&testing=${testing}`,
    {
      method: "GET",
    }
  );
  const data = await response.json();
  return data.reviews;
};

export const searchApis = async (name: string, hidePending: boolean = true) => {
  const response = await fetch(
    `${baseUrl}/service/search?name=${encodeURIComponent(name)}&hide_pending=${hidePending}`,
    {
      method: "GET",
    }
  );

  if (!response.ok) {
    const errorDetails = await response.text();
    console.error("Error in searchApis:", errorDetails);
    throw new Error(`Request failed with status ${response.status}`);
  }

  const data = await response.json();
  console.log("Search Results:", data);
  return data;
};


export const resetPasswordEmail = async (email: string) => {
  const response = await fetch(`${baseUrl}/auth/reset-password`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email }),
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || "Failed to send reset email.");
  }

  return data;
};



export const resetPassword = async (token: string, newPassword: string) => {
  const response = await fetch(`${baseUrl}/auth/reset-password/${token}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ newpass: newPassword }),
  });

  if (!response.ok) {
    throw new Error("Failed to reset password");
  }
};
