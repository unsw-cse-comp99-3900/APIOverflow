export interface Api {
  id: number;
  name: string;
  description: string;
  owner: string;
  icon_url: string;
  endpoint: string;
  tags: string[];
}

export type NewApi = Omit<Api, "id">;
