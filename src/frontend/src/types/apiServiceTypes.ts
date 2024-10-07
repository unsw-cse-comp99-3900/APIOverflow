import { Api, NewApi } from "./apiTypes";

export interface AddApiService {
    addApi: (newApi: NewApi) => Promise<void>;
}

export interface DeleteApiService {
    deleteApi: (api: Api) => Promise<void>;
}

export interface UpdateApiService {
    updateApi: (api: Api) => Promise<void>;
}

