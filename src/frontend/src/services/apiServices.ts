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
  ServiceApprove,
} from "../types/backendTypes";
import { Rating, Tag } from "../types/miscTypes";
import {
  adminUpdateDataFormatter,
  briefApiDataFormatter,
  permDataFormatter,
  userProfileDataFormatter,
  usersDataFormatter,
} from "../utils/dataFormatters";


let baseUrl = process.env.REACT_APP_API_BASE_URL;

/*        API Services        */
export const getApis = async (tags?: Tag[], hidePending = true) => {
  const queryParams =
    tags && tags.length > 0 ? `&tags=${tags.join("&tags=")}` : "";
  const response = await fetch(
    `${baseUrl}/service/filter?hide_pending=${hidePending}${queryParams}`,
    {
      method: "GET",
    }
  );
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
  console.log(data)
  return data.map(briefApiDataFormatter);
};

export const getApi = async (id: string) => {
  const response = await fetch(`${baseUrl}/service/get_service?sid=${id}`, {
    method: "GET",
  });
  const data = await response.json();
  console.log(data);
  if (response.status === 404) {
    throw new Error("Service Not Found");
  }
  return data;
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
  endpointLink: string
) => {
  const ParameterPlaceholder1: EndpointParameter = {
    id: "1",
    endpoint_link: endpointLink,
    required: false,
    type: "BODY",
    name: "Parameter Placeholder1",
    value_type: "string",
    example: "Example Placeholder1",
  };

  const ParameterPlaceholder2: EndpointParameter = {
    id: "2",
    endpoint_link: endpointLink,
    required: true,
    type: "HEADER",
    name: "Parameter Placeholder2",
    value_type: "string",
    example: "Example Placeholder2",
  };

  const ResponsePlaceholder1: EndpointResponse = {
    code: "200",
    description: "Description Placeholder1",
    conditions: ["Condition Placeholder1", "Condition Placeholder2"],
    example: "Example Placeholder1",
  };

  const ResponsePlaceholder2: EndpointResponse = {
    code: "404",
    description: "Description Placeholder2",
    conditions: ["Condition Placeholder1", "Condition Placeholder2"],
    example: "Example Placeholder2",
  };

  const endpoint1: Endpoint = {
    link: endpointLink,
    title_description: "Title Description Placeholder 1",
    main_description: "Main Description Placeholder 1",
    tab: "Tab Placeholder 1",
    parameters: [ParameterPlaceholder1, ParameterPlaceholder2],
    method: "GET",
    responses: [ResponsePlaceholder1, ResponsePlaceholder2],
  };

  const endpoint2: Endpoint = {
    link: endpointLink,
    title_description: "Title1 Description Placeholder 2",
    main_description: "Main Description Placeholder 2",
    tab: "Tab Placeholder 2",
    parameters: [ParameterPlaceholder1, ParameterPlaceholder2],
    method: "POST",
    responses: [ResponsePlaceholder1, ResponsePlaceholder2],
  };

  const endpoint3: Endpoint = {
    link: endpointLink,
    title_description: "Title1 Description Placeholder 3",
    main_description: "Main Description Placeholder 3",
    tab: "Tab Placeholder 3",
    parameters: [ParameterPlaceholder1, ParameterPlaceholder2],
    method: "PUT",
    responses: [ResponsePlaceholder1, ResponsePlaceholder2],
  };

  const endpoint4: Endpoint = {
    link: endpointLink,
    title_description: "Title1 Description Placeholder 4",
    main_description: "Main Description Placeholder 4",
    tab: "Tab Placeholder 4",
    parameters: [ParameterPlaceholder1, ParameterPlaceholder2],
    method: "DELETE",
    responses: [ResponsePlaceholder1, ResponsePlaceholder2],
  };

  const api: ServiceAdd = {
    name,
    description,
    endpoints: [endpoint1, endpoint2, endpoint3, endpoint4],
    tags,
    version_name: "1.0.0",
    version_description: "Initial Version",
    pay_model: "Free",
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

export const userLogout = async () => {
  await fetch(`${baseUrl}/auth/logout`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
    method: "POST",
  });
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

export const userCheckPerm = async () => {
  const response = await fetch(`${baseUrl}/user/permission_check`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
    method: "GET",
  });
  const data = await response.json();
  return permDataFormatter(data);
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
  await fetch(`${baseUrl}/service/add_icon`, {
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
  await fetch(`${baseUrl}/service/upload_docs`, {
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

/*        Admin Services       */
export const getPendingServices = async () => {
  const response = await fetch(`${baseUrl}/admin/get/services`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
    method: "GET",
  });
  const data = await response.json();
  return adminUpdateDataFormatter(data);
};

export const approveService = async (
  sid: string,
  approved: boolean,
  reason: string,
  serviceGlobal: boolean,
  versionName: string | null
) => {
  const approvalInfo: ServiceApprove = {
    sid,
    approved,
    reason,
    service_global: serviceGlobal,
    version_name: versionName,
  };
  console.log(approvalInfo);
  await fetch(`${baseUrl}/admin/service/approve`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(approvalInfo),
    method: "POST",
  });
};

export const userPromote = async (uid: string) => {
  console.log({
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({uid}),
    method: "POST",
  })
  const reponse = await fetch(`${baseUrl}/admin/promote?uid=${uid}`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
    },
    method: "POST",
  });
};

export const userDemote = async (uid: string) => {
  const reponse = await fetch(`${baseUrl}/admin/demote?uid=${uid}`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
    },
    method: "POST",
  });
};

export const userDelete = async (uid: string) => {
  const reponse = await fetch(`${baseUrl}/admin/delete/user?uid=${uid}`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
    },
    method: "DELETE",
  });
};

export const getUsers = async () => {
  const reponse = await fetch(`${baseUrl}/admin/dashboard/users`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
    },
    method: "GET",
  });
  const data = await reponse.json();
  return usersDataFormatter(data.users);
};

/*        User Services       */
export const getUser = async () => {
  const response = await fetch(`${baseUrl}/user/get`,
    {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
        "Content-Type": "application/json",
      },
      method: "GET"
    }
  );
  const data = await response.json();
  return userProfileDataFormatter(data);
}

export const getUserIcon = async () => {
  const response = await fetch(`${baseUrl}/user/get/icon`,
    {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
        "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
        Pragma: "no-cache",
        Expires: "0",
      },
      method: "GET",
    });
  const blob = await response.blob(); // Get the Blob data
  const url = URL.createObjectURL(blob); // Create a URL for the Blob
  return url;
}

export const updateDisplayName = async (displayName: string) => {
  const info = {
    content: displayName
  }
  const response = await fetch(`${baseUrl}/user/update/displayname`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(info)
    }
  );
  console.log(response.status);
  console.log(response.json());
}

export const userAddIcon = async (docId: string) => {
  const info = {
    doc_id: docId,
  };
  await fetch(`${baseUrl}/user/add_icon`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(info),
  });
};

/*        Misc Services       */
export const verifyEmail = async (token: string | null) => {
  const response = await fetch(`${baseUrl}/auth/verify-email/${token}`, {
    method: "POST",
  });
  return await response
}

export const searchApis = async (searchTerm: string, hidePending: boolean = true) => {
  try {
    const response = await fetch(
      `${baseUrl}/service/search?name=${encodeURIComponent(searchTerm)}`,
      {
        method: "GET",
        headers: {
          'Accept': 'application/json',
        }
      }
    );

    if (!response.ok) {
      throw new Error('Search failed');
    }

    const data = await response.json();
    return data.map(briefApiDataFormatter)
  } catch (error) {
    console.error('Search API error:', error);
    throw error;
  }
};

export const requestPasswordReset = async (email: string) => {
  const response = await fetch(`${baseUrl}/reset-password`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ content: email }),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to send reset email');
  }

  return response.json();
};

export const resetPasswordWithToken = async (token: string, newPassword: string) => {
  const response = await fetch(`${baseUrl}/auth/reset-password/${token}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ newpass: newPassword }),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to reset password');
  }

  return response.json();
};

export const submitReviewReply = async (reviewId: string, content: string) => {
  const response = await fetch(`${baseUrl}/review/reply`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      rid: reviewId,         // review ID
      content: content     // reply content
    }),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to submit reply');
  }

  return response.json();
};