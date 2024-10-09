// TODO: Define the types for the backend API
export interface BackendApi {
    id: number;
    name: string;
    description: string;
    owner_name: string;
    icon_url: string;
    tags: string[];
}