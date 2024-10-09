export function removeUnderscores<T>(obj: T): T {
  if (Array.isArray(obj)) {
    return obj.map((item) => removeUnderscores(item)) as unknown as T;
  } else if (typeof obj === "object" && obj !== null) {
    return Object.keys(obj).reduce((acc, key) => {
      const newKey = key.startsWith("_") ? key.slice(1) : key; // Remove leading underscore
      acc[newKey as keyof T] = removeUnderscores((obj as any)[key]);
      return acc;
    }, {} as T);
  }
  return obj;
}
