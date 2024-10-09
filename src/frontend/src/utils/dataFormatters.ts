// TODO: Change any to the correct backend API type
export const apiDataFormatter = (data:any) => {
    return {
        id: data.id,
        name: data.name,
        description: data.description,
        ownerName: data.owner.name,
        iconUrl: data.icon_url,
        tags: data.tags,
        documents: data.documents,
        endpoint: data.endpoint,
      }
}