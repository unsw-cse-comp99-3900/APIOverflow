// TODO: Define the types for the backend API



export interface ServicePost {
    name: string;
    description: string;
    icon_url: string;
    x_start:number;
    x_end: number;
    y_start: number;
    y_end: number;
    tags: string[];
    endpoint:string
}

export interface ServiceUpdate{
    sid: number;
    name: string;
    description: string;
    icon_url: string;
    x_start:number;
    x_end: number;
    y_start: number;
    y_end: number;
    tags: string[];
    endpoint:string
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