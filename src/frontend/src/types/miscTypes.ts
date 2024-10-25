export type Review = {
  reviewer: string;
  vote: boolean;
  content: string;
}

export type ServiceType = "api" | "micro"