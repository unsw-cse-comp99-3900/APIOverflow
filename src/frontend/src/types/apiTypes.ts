export interface Api {
  id: number;
  name: string;
  description: string;
  owner: string;
  icon_url: string;
  tags: string[];
  endpoint: string;
}

export type NewApi = Omit<Api, "id">;
