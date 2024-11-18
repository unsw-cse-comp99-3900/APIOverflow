export const briefApiDataFormatter = (data: any) => {
  return {
    id: data.id,
    name: data.name,
    description: data.description,
    owner: data.owner,
    tags: data.tags,
    documents: data.documents,
    endpoint: "yes",
  };
};

export const detailedApiDataFormatter = (data: any) => {
  return {
    id: data.id,
    name: data.name,
    description: data.description,
    owner: data.owner,
    tags: data.tags,
    docs: data.versions[0].docs,
    endpoint: data.versions[0].endpoints[0].link,
    reviews: data.reviews,
    upvotes: data.upvotes,
    type: data.type,
  };
};

export const permDataFormatter = (data: any) => {
  return {
    isAdmin: data.is_admin,
    isSuperAdmin: data.is_super,
  };
};

export const adminUpdateDataFormatter = (
  data: any
) => {
  return {
    newServices: data.new_services.map((service: any) => {
      return {
        id: service.id,
        name: service.name,
        description: service.description,
        serviceGlobal: true,
        versionName: service.version_fields.version_name
      };
    }),
    newVersions: data.version_updates.map((version: any) => {
      return {
        id: version.id,
        name: `${version.name}  |  ${version.version_name}`,
        description: version.version_description,
        serviceGlobal: false,
        versionName: version.version_name,
      };
    }),
    generalInfoUpdates: data.global_updates.map((service: any) => {
      return {
        id: service.id,
        name: service.name,
        description: service.description,
        serviceGlobal: true,
        versionName: null
      };
    }),
  };
};

export const usersDataFormatter = (data: any) => {
  return data.map((user: any) => {
    let role = "General User";
    
    if (user.is_super) {
      role = "Super Admin";
    } else if (user.is_admin) {
      role = "Admin";
    }

    return {
      id: user.id,
      name: user.displayname,
      role
    };
  });
}