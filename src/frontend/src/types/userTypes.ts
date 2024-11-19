export interface User {
  id: number;
  name: string;
  email: string;
  displayName: string;
}

export interface UserBrief {
  id: string;
  name: string;
  role: "General User" | "Admin" | "Super Admin";
}

export interface serviceOwner {
  id: number;
  name: string;
  displayName: string;
  email: string;
}

export interface UserProfile {
  id: string;
  username: string;
  email: string;
  displayName: string;
  icon: string;
  role: string;
}