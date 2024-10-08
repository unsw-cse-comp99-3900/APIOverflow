import React from 'react'
import { FaArrowLeft } from 'react-icons/fa'
import { Link } from 'react-router-dom'

const BackButton = ( {toUrl}: {toUrl:string} ) => {
  return (
    <div className="container m-auto py-6 px-6">
    <Link
      to={toUrl}
      className="text-blue-800 hover:text-indigo-500 hover:underline font-bold flex items-center"
    >
      <FaArrowLeft className="mr-2" /> Back
    </Link>
  </div>
  )
}

export default BackButton