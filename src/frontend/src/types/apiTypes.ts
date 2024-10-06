export interface Api {
    id: string;
    sid: string;
    name: string;
    description: string;
    owner: string;
    icon_url: string;
    tags: string[]; 
}

export type NewApi = Omit<Api, 'id' | 'sid'>;