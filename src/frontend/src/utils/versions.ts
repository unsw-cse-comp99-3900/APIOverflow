import { Version } from "../types/apiTypes";

export function getCurrVersions(versions: Version[]): Version[] {
  return versions.filter((version) => !version.newly_created);
}