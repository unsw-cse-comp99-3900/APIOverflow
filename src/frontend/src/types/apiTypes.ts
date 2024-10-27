import { Review, ServiceType } from "./miscTypes";

export interface BriefApi {
  id: string;
  name: string;
  description: string;
  owner: string;
  iconUrl: string;
  tags: string[];
}

export type DetailedApi = BriefApi & {
  docs: string[];
  endpoint: string;
  reviews: Review[];
  upvotes: number;
  type: ServiceType;
}

export type NewApi = Omit<DetailedApi, "id">;