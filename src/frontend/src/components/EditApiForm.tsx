import React, { useState } from 'react'
import EndpointsSidebar from './EndPointsSideBar'
import { Endpoint } from '../types/backendTypes';

const EditApiForm = ({ apiId }: { apiId?: string }) => {
  const [endpoints, setEndpoints] = useState<Endpoint[]>([]);

  return (
    <div>
      <EndpointsSidebar endpoints={endpoints} setEndpoints={setEndpoints}/>
      EditApiForm</div>
  )
}

export default EditApiForm