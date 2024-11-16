export const briefApiDataFormatter = (data:any) => {
    return {
        id: data.id,
        name: data.name,
        description: data.description,
        owner: data.owner,
        tags: data.tags,
        documents: data.documents,
        endpoint: "yes",
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
        endpoint: data.versions[0].endpoints[0].link,
        reviews: data.reviews,
        upvotes: data.upvotes,
        type: data.type,
      }
}