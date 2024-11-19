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

export type Rating = "positive" | "negative"

export type Tag = string

export type ServiceType = "api" | "micro"

export type Status = "pending" | "approved" | "rejected"

export type PayModel = "Free" | "Freemium" | "Premium"

export type AllowedEndpointTypes = "GET" | "POST" | "PUT" | "DELETE"

export type AllowedParameterTypes = "HEADER" | "BODY" | "PATH" | "QUERY"