import { Endpoint } from "./backendTypes";
import { Review, ServiceType } from "./miscTypes";
import { serviceOwner } from "./userTypes";

export interface BriefApi {
  id: string;
  name: string;
  description: string;
  owner: string;
  tags: string[];
}

export type ServiceStatus =
  | "LIVE"
  | "PENDING"
  | "REJECTED"
  | "UPDATE_PENDING"
  | "UPDATE_REJECTED";

export type DetailedApi = {
  description: string;
  downvotes: number;
  upvotes: number;
  icon: string;
  icon_url: string;
  id: string;
  name: string;
  owner: serviceOwner;
  pay_model: "Free" | "Paid";
  reviews: Review[];
  status:ServiceStatus;
  tags: string[];
  type: ServiceType;
  versions: Version[];
};

export type Version = {
  docs: string[];
  endpoints: Endpoint[];
  newly_created: boolean;
  status: ServiceStatus;
  status_reason: string;
  version_description:string;
  version_name: string;
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
