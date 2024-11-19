import React from 'react'


interface VersionInfoOverlayProps {
  isOpen: boolean;
  onRequestClose: () => void;
  serviceName: string;
  actionType: "approve" | "reject";
  onSubmit: (reason: string) => void;
}

const VersionInfoOverlay:React.FC<VersionInfoOverlayProps> = () => {
  return (
    <div>VersionInfoOverlay</div>
  )
}

export default VersionInfoOverlay