import React, { createContext, useContext, useState, ReactNode } from "react";
import { Tag } from "../types/miscTypes";

interface SelectedTagsContextProps {
  selectedTags: string[];
  toggleTag: (tag: Tag) => void;
  clearTags: () => void;
}

const SelectedTagsContext = createContext<SelectedTagsContextProps | null>(
  null
);

export const useSelectedTags = () => {
  const context = useContext(SelectedTagsContext);
  if (!context) {
    throw new Error("useSelectedTags must be used within a SelectedTagsProvider");
  }
  return context;
};

export const SelectedTagsProvider = ({ children }: { children: ReactNode }) => {
  const [selectedTags, setSelectedTags] = useState<Tag[]>([]);

  const toggleTag = (tag: Tag) => {
    setSelectedTags((prevSelected) =>
      prevSelected.includes(tag)
        ? prevSelected.filter((prevTag) => prevTag !== tag)
        : [...prevSelected, tag]
    );
  };

  const clearTags = () => {
    setSelectedTags([]);
  };

  return (
    <SelectedTagsContext.Provider value={{ selectedTags, toggleTag, clearTags }}>
      {children}
    </SelectedTagsContext.Provider>
  );
};
