import { Api } from "./apiTypes";

export interface AddApiService {
    addApi: (newApi: Omit<Api, 'id' | 'sid'>) => Promise<void>;
}

export interface DeleteApiService {
    deleteApi: (api: Api) => Promise<void>;
}

export interface UpdateApiService {
    updateApi: (api: Api) => Promise<void>;
}

