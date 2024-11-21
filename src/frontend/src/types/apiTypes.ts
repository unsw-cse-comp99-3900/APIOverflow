import { Endpoint } from "./backendTypes";
import { PayModel, Review, ServiceType } from "./miscTypes";
import { serviceOwner } from "./userTypes";

export interface BriefApi {
  id: string;
  name: string;
  description: string;
  owner: string;
  tags: string[];
  payModel: PayModel;
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
  id: string;
  name: string;
  owner: serviceOwner;
  pay_model: PayModel;
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

export type PendingVersion = Version & {
  id: string;
}

export type PendingGeneralInfo = {
  description: string;
  id: string;
  name: string;
  tags: string[];
}

export type PendingNewService = {
  id: string;
  name: string;
  description: string;
  pay_model: PayModel;
  tags: string[];
  version_fields: PendingVersion;
}

export type NewApi = Omit<DetailedApi, "id">;
