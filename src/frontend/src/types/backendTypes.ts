import { Rating } from "./miscTypes";

export interface ServicePost {
    name: string;
    icon_url: string;
    description: string;
    x_start:number;
    x_end: number;
    y_start: number;
    y_end: number;
    tags: string[];
    endpoint:string
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
  