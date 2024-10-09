export interface Api {
  id: number;
  name: string;
  description: string;
  ownerName: string;
  iconUrl: string;
  tags: string[];
  endpoint: string;
}

export type DetailedApi = Api & {
  documents: string[];

}

export type NewApi = Omit<DetailedApi, "id">;