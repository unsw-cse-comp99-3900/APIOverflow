import { Version } from "../types/apiTypes";

export function notNewVersions(versions: Version[]): Version[] {
  return versions.filter((version) => !version.newly_created);
}