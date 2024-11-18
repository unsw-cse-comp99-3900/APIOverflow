import React from 'react'
import { Endpoint } from '../types/backendTypes';

interface EndpointUpdateFormProps {
  currEndpoint: Endpoint;
  setcurrEndpoint: React.Dispatch<React.SetStateAction<Endpoint>>;
}

const EndpointUpdateForm: React.FC<EndpointUpdateFormProps> = (currEndpoint, setCurrEndpoint) => {
  return (
    <div>EndpointUpdateForm</div>
  )
}

export default EndpointUpdateForm