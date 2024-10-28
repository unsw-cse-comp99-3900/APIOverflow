export const briefApiDataFormatter = (data:any) => {
    return {
        id: data.id,
        name: data.name,
        description: data.description,
        owner: data.owner,
        tags: data.tags,
        documents: data.documents,
        endpoint: data.endpoint,
      }
}

export const detailedApiDataFormatter = (data:any) => {
    return {
        id: data.id,
        name: data.name,
        description: data.description,
        owner: data.owner,
        tags: data.tags,
        docs: data.docs,
        endpoint: data.endpoint,
        reviews: data.reviews,
        upvotes: data.upvotes,
        type: data.type,
      }
}