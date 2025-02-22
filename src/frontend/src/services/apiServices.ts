import { DetailedApi } from "../types/apiTypes";
import {
  Endpoint,
  LoginModel,
  EndpointParameter,
  ServiceIconInfo,
  ServiceAdd,
  ServiceReviewInfo,
  ServiceGlobalUpdate,
  ServiceUpload,
  TagData,
  UserCreate,
  EndpointResponse,
  ServiceApprove,
} from "../types/backendTypes";
import { PayModel, Rating, Tag } from "../types/miscTypes";
import {
  adminUpdateDataFormatter,
  briefApiDataFormatter,
  permDataFormatter,
  userProfileDataFormatter,
  usersDataFormatter,
} from "../utils/dataFormatters";

let baseUrl = process.env.REACT_APP_API_BASE_URL;

/*        API Services        */
export const getApis = async (tags?: Tag[], hidePending = true, sortRating = true) => {
  const queryParams =
    tags && tags.length > 0 ? `&tags=${tags.join("&tags=")}` : "";
  const response = await fetch(
    `${baseUrl}/service/filter?hide_pending=${hidePending}${queryParams}`,
    {
      method: "GET",
    }
  );
  const data = await response.json();
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
  return data.map(briefApiDataFormatter);
};

export const getApi = async (id: string) => {
  const response = await fetch(`${baseUrl}/service/get_service?sid=${id}`, {
    method: "GET",
  });
  const data = await response.json();
  if (response.status === 404) {
    throw new Error("Service Not Found");
  }
  return data;
};

export const deleteApi = async (id: string) => {
  await fetch(`${baseUrl}/service/delete?sid=${id}`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
    },
    method: "DELETE",
  });
  return;
};

export const addApi = async (api: ServiceAdd) => {
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

export const updateServiceGlobal = async (
  name: string,
  description: string,
  tags: string[],
  pay_model: PayModel,
  sid: string
) => {
  const api: ServiceGlobalUpdate = {
    sid,
    name,
    description,
    pay_model,
    tags,
  };
  const response = await fetch(`${baseUrl}/service/update`, {
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
  return;
};

export const addNewVersion = async (
  sid:string,
  versionName:string,
  versionDescription:string,
  endpoints:Endpoint[],
) => {
  const newVersion = {
    sid,
    version_name: versionName,
    version_description: versionDescription,
    endpoints,
  };
  
  const response = await fetch(`${baseUrl}/service/version/add`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(newVersion),
  });

  if (response.status === 401) {
    throw new Error("Unauthorized");
  } else if (response.status === 404) {
    throw new Error("PendingService");
  }
  return;
}

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
  const response = await fetch(`${baseUrl}/auth/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(newUser),
  });

  if (response.status === 400) {
    throw new Error("DuplicateCredentials");
  }
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
export const getTags = async (system: boolean = false) => {  
  const response = await fetch(`${baseUrl}/tags/get?system=${system}`, {
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

export const apiGetOwner = async (sid: string) => {
  const response = await fetch(`${baseUrl}/service/get_service?sid=${sid}`, {
    method: "GET",
  });
  const data = await response.json();
  return data.owner.id;
}

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
export const uploadDocs = async (sid: string, docId: string, versionName: string) => {
  const info: ServiceUpload = {
    sid,
    version_name: versionName,
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
  if(response.status === 401){
    throw new Error("Unauthorized");
  }

  if (response.status === 403) {
    throw new Error(data.detail);
  }
};

export const apiGetReviews = async (sid: string, filter: string = "") => {
  let u_toggle;
  if (localStorage.getItem("token")) {
    const res = await fetch(`${baseUrl}/user/get/id`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });
    const data = await res.json();
    u_toggle = data.uid;
  } else {
    u_toggle = "";
  }
  const url = `${baseUrl}/service/get/reviews?sid=${sid}&filter=${filter}&uid=${u_toggle}`;
  const response = await fetch(url);
  const data = await response.json();
  return data.reviews;
};


export const apiGetRating = async (sid: string) => {
  const response = await fetch(`${baseUrl}/service/get/rating?sid=${sid}`, {
    method: "GET",
  });
  const data = await response.json();
  return data.rating;
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
  return data;
};

export const approveNewService = async (
  sid: string,
  approved: boolean,
  reason: string,
  versionName: string
) => {
  const approvalInfo: ServiceApprove = {
    sid,
    approved,
    reason,
    service_global: true,
    version_name: versionName,
  };

  await fetch(`${baseUrl}/admin/service/approve`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(approvalInfo),
    method: "POST",
  });
};

export const approveNewVersion = async (
  sid: string,
  approved: boolean,
  reason: string,
  versionName: string
) => {
  const approvalInfo: ServiceApprove = {
    sid,
    approved,
    reason,
    service_global: false,
    version_name: versionName,
  };

  await fetch(`${baseUrl}/admin/service/approve`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(approvalInfo),
    method: "POST",
  });
};

export const approveGeneralInfo = async (
  sid: string,
  approved: boolean,
  reason: string,
) => {
  const approvalInfo: ServiceApprove = {
    sid,
    approved,
    reason,
    service_global: true,
  };

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
  const reponse = await fetch(`${baseUrl}/admin/promote?uid=${uid}`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
    },
    method: "POST",
  });
};

export const userDemote = async (uid: string) => {
  const response = await fetch(`${baseUrl}/admin/demote?uid=${uid}`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
    },
    method: "POST",
  });

  return response.ok;
};

export const userDelete = async (uid: string) => {
  const response = await fetch(`${baseUrl}/admin/delete/user?uid=${uid}`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
    },
    method: "DELETE",
  });

  return response.ok;
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
  const response = await fetch(`${baseUrl}/user/get`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
    },
    method: "GET",
  });
  if (response.status === 401) {
    throw new Error("Unauthorized");
  }
  const data = await response.json();
  return userProfileDataFormatter(data);
};

export const getUserIcon = async () => {
  const response = await fetch(`${baseUrl}/user/get/icon`, {
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
};

export const updateDisplayName = async (displayName: string) => {
  const info = {
    content: displayName,
  };
  const response = await fetch(`${baseUrl}/user/update/displayname`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(info),
  });
};

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

export const userGetReviews = async () => {
  const response = await fetch(`${baseUrl}/user/get/reviews`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
  });
  const data = await response.json()
  return data.reviews
}

export const userEditReview = async (id: string, rting: Rating | null, comment: string) => {
  const info = {
    rid: id,
    rating: String(rting),
    comment: comment,
  };
  
  const response = await fetch(`${baseUrl}/review/edit`,  {
      method: "POST",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(info),
    }
  );
}

export const userDeleteReview = async (rid: string) => {
  await fetch(`${baseUrl}/review/delete?rid=${rid}`,  {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
  }
  );
}

export const userUpvoteReview = async(rid: string) => {
  const response = await fetch(`${baseUrl}/review/upvote`,{
    method: "POST",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      rid: rid,
      content: ""
    })
  });
  if (!response.ok) {
    return false;
  } else {
    return true;
  }
}

export const userDownvoteReview = async(rid: string) => {
  const response = await fetch(`${baseUrl}/review/downvote`,{
    method: "POST",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      rid: rid,
      content: ""
    })
  });

  if (!response.ok) {
    return false;
  } else {
    return true;
  }
}

export const userRemoveVote = async(rid: string) => {
  await fetch(`${baseUrl}/review/remove_vote`,{
    method: "POST",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      rid: rid,
      content: ""
    })
  })
}

export const userGetId = async () => {
  if (localStorage.getItem("token")) { 
    const res = await fetch(`${baseUrl}/user/get/id`,
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      }
    );
    const data = await res.json();
    return data.uid;
  } else {
    return "";
  }
}

export const userGetReplies = async () => {
  const response = await fetch(`${baseUrl}/user/get/replies`,{
    method: "GET",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
  });
  const data = await response.json();
  return data.replies;
}

export const userDeleteReply = async (rid: string) => {
  await fetch(`${baseUrl}/review/reply/delete?rid=${rid}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    }
  });
};

export const userEditReply = async (rid: string, content: string) => {
  const response = await fetch(`${baseUrl}/review/reply/edit`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      rid,
      content,
    })
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to edit reply');
  }
};

/*        Misc Services       */
export const verifyEmail = async (token: string | null) => {
  const response = await fetch(`${baseUrl}/auth/verify-email/${token}`, {
    method: "POST",
  });
  return await response;
};

export const searchApis = async (
  searchTerm: string,
  hidePending: boolean = true
) => {
  try {
    const response = await fetch(
      `${baseUrl}/service/search?name=${encodeURIComponent(searchTerm)}`,
      {
        method: "GET",
        headers: {
          Accept: "application/json",
        },
      }
    );

    if (!response.ok) {
      throw new Error("Search failed");
    }

    const data = await response.json();
    return data.map(briefApiDataFormatter);
  } catch (error) {
    console.error("Search API error:", error);
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


interface ReviewPackage {
  rid: string;
  content: string;
}

export const submitReviewReply = async (rid: string, content: string) => {
  const reviewPackage: ReviewPackage = {
    rid,
    content
  };

  try {
    const response = await fetch(`${baseUrl}/review/reply`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(reviewPackage),
    });
    if (!response.ok) {
      const errorData = await response.json();
      console.error('Error response:', errorData);
      throw new Error(errorData.detail || 'Failed to submit reply');
    }

    return response.json();
  } catch (error) {
    console.error('Reply submission error:', error);
    throw error;
  }
};

export const getReplyService = async (rid: string) => {
  const response = await fetch(`${baseUrl}/review/reply/get?rid=${rid}`, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    }
  });

  if (!response.ok) {
    throw new Error('Failed to fetch reply');
  }

  return response.json();
};

export const getCustomTags = async () => {
  const response = await fetch(`${baseUrl}/tags/get/ranked?num=${-1}&custom=${true}`,{
    method: "GET",
  });
  const data = await response.json();
  return data.tags;
}

export const fetchReviews = async (sid: string, filter: boolean = false, sort: 'best' | 'worst' = 'best') => {
  try {
    const u_toggle = await userGetId();
    
    const url = `${baseUrl}/service/get/reviews?sid=${sid}&filter=${sort}&uid=${u_toggle}`;
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Failed to fetch reviews');
    }

    const data = await response.json();
    return data.reviews;
  } catch (error) {
    console.error('Error fetching reviews:', error);
    throw error;
  }
};


export const uploadYAML = async (file: File) => {
  const formData = new FormData();
  formData.append("file", file);
  try {
    const response = await fetch(`${baseUrl}/service/yaml`, {
      method: "POST",
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
      body: formData,
    });

    if (!response.ok) {
      return '';
    }

    const data = await response.json();
    return data.id;
  } catch (error) {
    console.error('Bad file');
    throw error;
  }
}