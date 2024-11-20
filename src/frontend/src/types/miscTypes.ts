export type Review = {
  rid: string;
  reviewer: string; // uid
  reviewerName: string;
  service: string; // sid
  title: string;
  comment: string;
  type: Rating;
  upvotes: string;
  downvotes: string;
  timestamp: string;
  e_timestamp: string;
  edited: boolean;
  voted: string;
}

export type ReviewDetail = {
  rid: string;
  reviewer: string; // uid
  reviewerName: string;
  service: string; // sid
  comment: string;
  type: Rating;
  upvotes: string;
  downvotes: string;
}

export type ReplyDetail = {
  rid: string;
  reviewerName: string;
  service: string;
  comment: string;
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