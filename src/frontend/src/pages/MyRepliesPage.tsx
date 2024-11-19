import { PhotoIcon } from "@heroicons/react/24/solid";
import React, { useState, useEffect } from 'react'
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { UserProfile } from "../types/userTypes";
import {
  getUser,
  updateDisplayName,
  uploadImage,
  userAddIcon,
} from "../services/apiServices";

const MyRepliesPage = () => {
  const navigate = useNavigate();
    return (
        <div>
            My RepliesPage
        </div>
    )
}

export default MyRepliesPage;