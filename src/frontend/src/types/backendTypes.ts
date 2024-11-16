import { AllowedEndpointTypes, AllowedParameterTypes, Rating } from "./miscTypes";

export interface ServiceAdd {
    name: string;
    description: string;
    tags: string[];
    endpoints: Endpoint[];
}

export interface ServiceUpdate{
    name: string;
    description: string;
    tags: string[];
    endpoint:string
    sid: string;
}

export interface LoginModel {
    username: string;
    password: string;
}

export interface UserCreate {
    username: string;
    password: string;
    displayname: string;
    email: string;
}

export interface TagData {
    tag: string;
}

export interface ServiceIconInfo {
    sid: string;
    doc_id: string;
}

export interface ServiceUpload {
    sid: string;
    doc_id: string;
}

export interface ServiceReviewInfo {
    sid: string;
    rating: Rating;
    title: string;
    comment: string;
}

export interface Review {
    id: string;
    rid: string; // Review ID
    service: string;
    title: string;
    type: Rating;
    reviewer: string;
    comment: string;
    status: string;
  }

export interface Endpoint{
    link: string;
    title_description: string;
    main_description: string;
    tab: string;
    parameters: EndpointParameter[];
    method: AllowedEndpointTypes;
    responses: EndpointResponse[];
}

export interface EndpointParameter{
    id: string;
    endpoint_link: string;
    required: boolean;
    type: AllowedParameterTypes;
    name: string;
    value_type: string
    example: string;
}

export interface EndpointResponse{
    code: string;
    description: string;
    conditions: string[];
    example: string
}