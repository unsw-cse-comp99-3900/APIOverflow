export type Review = {
  id: string;
  rid: string;
  reviewer: string; // uid
  reviewerName: string;
  service: string; // sid
  title: string;
  comment: string;
  type: Rating;
  status: Status;
}

export type ReviewDetail = {
  id: string;
  rid: string;
  reviewer: string; // uid
  reviewerName: string;
  service: string; // sid
  title: string;
  comment: string;
  type: Rating;
  status: Status;
  upvotes: string;
  downvotes: string;
}

export type Rating = "positive" | "negative"

export type Tag = string

export type CustomTag = {
  tid: string;
  tag: string;
  type: number;
  num: number;
}

export type ServiceType = "api" | "micro"

export type Status = "pending" | "approved" | "rejected"

export type PayModel = "Free" | "Freemium" | "Premium"

export type AllowedEndpointTypes = "GET" | "POST" | "PUT" | "DELETE"

export type AllowedParameterTypes = "HEADER" | "BODY" | "PATH" | "QUERY"