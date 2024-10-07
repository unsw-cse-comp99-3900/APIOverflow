import React from 'react';
import { Link } from 'react-router-dom';

interface TagProps {
  tag: string;
  className?: string; // Allow className as an optional prop
}

const Tag: React.FC<TagProps> = ({ tag, className }) => {
  return (
    <Link to={`/apis`} className={className}>
      <span className={`bg-gray-300 hover:bg-blue-950 text-black hover:text-white text-sm font-bold px-3 py-1 rounded-md cursor-pointer`}>
        {tag}
      </span>
    </Link>
  );
};

export default Tag;
