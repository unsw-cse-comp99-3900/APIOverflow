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
    email: string;
}

export interface TagData {
    tag: string;
}

export interface ServiceIconInfo {
    sid: string;
    doc_id: string;
}