import React, { useState } from "react";
import { Outlet } from "react-router-dom";
import TagsSideBar from "../components/TagsSideBar";

const TagsSidebarLayout: React.FC = () => {
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  return (
    <div className="flex">
      <TagsSideBar
        selectedTags={selectedTags}
        setSelectedTags={setSelectedTags}
      />
      <section className="flex-1 ml-80">
        <Outlet context={{ selectedTags }} />
      </section>
    </div>
  );
};

export default TagsSidebarLayout;
