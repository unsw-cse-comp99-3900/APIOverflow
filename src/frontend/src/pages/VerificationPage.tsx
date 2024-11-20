import React, { useState, useEffect } from "react";
import { Link, useNavigate, useLocation, useSearchParams  } from "react-router-dom";

// Import the blob SVG
import Blob1 from "../assets/images/blobs/blob1.svg";
import Blob2 from "../assets/images/blobs/blob2.svg";

// Import verification route
import { verifyEmail } from "../services/apiServices";

const VerificationPage: React.FC = () => {
  const location = useLocation();
  const [bigMsg, setBigMsg] = useState("");
  const [smallMsg, setSmallMsg] = useState("Verifying...");
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();
  let [searchParams, setSearchParams] = useSearchParams();
  let token = searchParams.get("token")

    useEffect(() => {
      let ignore = false;
    
      if (!ignore)  verifyProcess()
    return () => { ignore = true; }
    },[]);
    
    const verifyProcess = async (...args: never[]) =>  {
        try {
            const res = await verifyEmail(token)
            setIsLoading(false);
            if (!res.ok) { // Something happened here.
                setSmallMsg(`Something went wrong in the verification process. Please try again later!`);

            } else {
              setBigMsg("Welcome to APIOverflow!");
              setSmallMsg(`Email verified. You may now log in.`)
            }
            
          } catch (error) {

          }
    }

  return (
    <div className="relative w-screen h-screen pt-24">
      <div className="h-full pt-24 bg-gradient-to-b from-blue-900 to-[#63b3de] flex justify-center items-center">
        {/* Add the blob as an SVG image   */}
        <img
          src={Blob1}
          alt="Blob 1"
          className="absolute top-24 right-0 w-[400px] h-auto"
        />
        <img
          src={Blob2}
          alt="Blob 2"
          className="absolute bottom-0 left-0 w-[400px] h-auto"
        />

        {/* Verify Message Box */}
        <div className="w-full max-w-md bg-white rounded-lg shadow-lg p-8 z-10">
            {isLoading ? (
                <div className="flex flex-col items-center text-center">
                    <div
                    className="spinner-border animate-spin inline-block w-8 h-8 border-4 rounded-full mb-2"
                    role="status"
                    ></div>
                    <span className="visually-hidden">Verifying...</span>
                </div>
                ) : (
                <div>
                  <div className = "flex items-center">
                    <h1 className="text-3xl font-bold text-center text-blue-900">{bigMsg}</h1>  
                  </div>
                  <div className = "flex items-center">
                    <h1 className="text-2xl font-bold text-center text-blue-900">{smallMsg}</h1>    
                  </div> 
                </div>  
                )}
        </div>
      </div>
    </div>
  );
};

export default VerificationPage;
