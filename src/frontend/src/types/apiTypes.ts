import { Endpoint } from "./backendTypes";
import { Review, ServiceType } from "./miscTypes";

export interface BriefApi {
  id: string;
  name: string;
  description: string;
  owner: string;
  tags: string[];
}

export type DetailedApi = BriefApi & {
  docs: string[];
  endpoint: string;
  reviews: Review[];
  upvotes: number;
  type: ServiceType;
};

export interface ServiceAdminBrief {
  id: string;
  name: string;
  serviceGlobal: boolean;
  versionName: string | null;
  description: string;
}

export interface ServiceUpdateDataAdminView {
  newServices: ServiceAdminBrief[];
  newVersions: ServiceAdminBrief[];
  generalInfoUpdates: ServiceAdminBrief[];
}

export type NewApi = Omit<DetailedApi, "id">;
