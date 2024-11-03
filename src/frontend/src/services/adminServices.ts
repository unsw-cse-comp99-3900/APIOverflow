// src/services/adminServices.ts

let baseUrl = process.env.REACT_APP_API_BASE_URL;

/*        User Management Services       */

// Fetch all users
export const fetchAllUsers = async () => {
  const response = await fetch(`${baseUrl}/admin/users`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
  });
  if (!response.ok) {
    const errorDetails = await response.text();
    console.error("Error:", errorDetails);
    throw new Error(`Request failed with status ${response.status}`);
  }

  const data = await response.json();
  return data.users;
};

// Promote a user to admin
export const promoteUser = async (userId: string) => {
  const response = await fetch(`${baseUrl}/admin/users/promote/${userId}`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    const errorDetails = await response.text();
    console.error("Error:", errorDetails);
    throw new Error(`Request failed with status ${response.status}`);
  }
};

// Demote a user from admin
export const demoteUser = async (userId: string) => {
  const response = await fetch(`${baseUrl}/admin/users/demote/${userId}`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    const errorDetails = await response.text();
    console.error("Error:", errorDetails);
    throw new Error(`Request failed with status ${response.status}`);
  }
};

// Delete a user
export const deleteUser = async (userId: string) => {
  const response = await fetch(`${baseUrl}/admin/users/delete/${userId}`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
  });

  if (!response.ok) {
    const errorDetails = await response.text();
    console.error("Error:", errorDetails);
    throw new Error(`Request failed with status ${response.status}`);
  }
};

/*        Service Management Services       */

// Fetch pending services
export const fetchPendingServices = async (status: string = "ALL_PENDING") => {
  const response = await fetch(`${baseUrl}/admin/services?status=${status}`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
  });

  if (!response.ok) {
    const errorDetails = await response.text();
    console.error("Error:", errorDetails);
    throw new Error(`Request failed with status ${response.status}`);
  }

  const data = await response.json();
  return data.services;
};

// Approve a service
export const approveService = async (serviceId: string) => {
  const response = await fetch(`${baseUrl}/admin/services/approve/${serviceId}`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    const errorDetails = await response.text();
    console.error("Error:", errorDetails);
    throw new Error(`Request failed with status ${response.status}`);
  }
};

// Reject a service with a reason
export const rejectService = async (serviceId: string, reason: string) => {
  const response = await fetch(`${baseUrl}/admin/services/reject/${serviceId}`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ reason }),
  });

  if (!response.ok) {
    const errorDetails = await response.text();
    console.error("Error:", errorDetails);
    throw new Error(`Request failed with status ${response.status}`);
  }
};

/*        Review Management Services       */

// Fetch pending reviews
export const fetchPendingReviews = async (status: string = "PENDING") => {
  const response = await fetch(`${baseUrl}/admin/reviews?status=${status}`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
  });

  if (!response.ok) {
    const errorDetails = await response.text();
    console.error("Error:", errorDetails);
    throw new Error(`Request failed with status ${response.status}`);
  }

  const data = await response.json();
  return data.reviews;
};

// Approve a review
export const approveReview = async (reviewId: string) => {
  const response = await fetch(`${baseUrl}/admin/reviews/approve/${reviewId}`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    const errorDetails = await response.text();
    console.error("Error:", errorDetails);
    throw new Error(`Request failed with status ${response.status}`);
  }
};

// Reject a review with a reason
export const rejectReview = async (reviewId: string, reason: string) => {
  const response = await fetch(`${baseUrl}/admin/reviews/reject/${reviewId}`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ reason }),
  });

  if (!response.ok) {
    const errorDetails = await response.text();
    console.error("Error:", errorDetails);
    throw new Error(`Request failed with status ${response.status}`);
  }
};
