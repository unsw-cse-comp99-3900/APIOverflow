import React from 'react';

interface FullScreenOverlayProps {
  isOpen: boolean;
  onClose: () => void;
}

const TagsOverlay: React.FC<FullScreenOverlayProps> = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-70 flex justify-center items-center z-50">
      <div className="relative bg-white rounded-lg shadow-lg w-11/12 max-w-4xl p-6 overflow-y-auto max-h-[90vh]">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-3 right-4 text-gray-600 hover:text-gray-800 text-2xl font-bold"
        >
          &times;
        </button>
        
        {/* Overlay Content */} 
        <div className="text-left">
          <h2 className="text-2xl font-semibold text-blue-800 mb-4">Tags</h2>
          <p>This is an example of a full-screen overlay using Tailwind CSS.</p>
          
          {/* Add more content as per your design */}
        </div>
      </div>
    </div>
  );
};

export default TagsOverlay;
