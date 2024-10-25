import React from "react";
import { Outlet, useOutletContext } from "react-router-dom";
import TagsSideBar from "../components/TagsSideBar";

interface OutletContext {
  selectedTags: string[];
  setSelectedTags: React.Dispatch<React.SetStateAction<string[]>>;
}

const TagsSidebarLayout: React.FC = () => {

  const { selectedTags, setSelectedTags } = useOutletContext<OutletContext>();
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
