import React from "react";
import { FaFilePdf } from "react-icons/fa";

interface FileCardProps {
  fileName: string;
}

const FileCard:React.FC<FileCardProps> = ({ fileName }) => {
  return (
    <div className="flex items-center mt-4 p-4 border border-gray-300 rounded-lg shadow-md bg-white">
      <FaFilePdf className="text-red-600 text-3xl mr-3" />
      <div>
        <p className="text-lg font-medium text-gray-800">{fileName}</p>
      </div>
    </div>
  );
};

export default FileCard;
