import React from "react";
import { Link } from "react-router-dom";

interface TagProps {
  tag: string;
  className?: string; // Allow className as an optional prop
}

const Tag: React.FC<TagProps> = ({ tag, className }) => {
  return (
    <Link to={`/apis`} className={className}>
      <span
        className={`bg-blue-800 hover:bg-amber-200 text-white hover:text-black text-sm font-semibold px-3 py-1 rounded-md cursor-pointer`}
      >
        {tag}
      </span>
    </Link>
  );
};

export default Tag;
