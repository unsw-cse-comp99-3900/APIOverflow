import React, { useEffect, useState } from "react";
import EndpointsSidebar from "./EndPointsSideBar";
import { Endpoint } from "../types/backendTypes";
import OverviewUpdateForm from "./OverviewUpdateForm";
import EndpointUpdateForm from "./EndpointUpdateForm";
import {
  addApi,
  addTag,
  apiAddIcon,
  getApi,
  updateApi,
  uploadDocs,
  uploadImage,
  uploadPDF,
} from "../services/apiServices";
import { toast } from "react-toastify";
import { PayModel, Tag } from "../types/miscTypes";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { DetailedApi } from "../types/apiTypes";
import VersionInfoOverlay from "./VersionInfoOverlay";

const EditApiForm = ({ apiId }: { apiId?: string }) => {
  // General Info
  const [api, setApi] = useState<DetailedApi | null>(null);
  const [name, setName] = useState<string>("");
  const [description, setDescription] = useState<string>("");
  const [selectedTags, setSelectedTags] = useState<Tag[]>(["API"]);
  const [newTags, setNewTags] = useState<Tag[]>([]);
  const [payModel, setPayModel] = useState<PayModel>("Free");
  const [selectedImage, setSelectedImage] = useState<string>("");
  const [selectedImageData, setSelectedImageData] = useState<File | null>(null);

  // Verion Info
  const [endpoints, setEndpoints] = useState<Endpoint[]>([]);
  const [versionUpdated, setVersionUpdated] = useState<boolean>(false);
  const [versionName, setVersionName] = useState<string>("");
  const [versionDescription, setVersionDescription] = useState<string>("");
  const [isVersionInfoOverlayOpen, setIsVersionInfoOverlayOpen] =
    useState<boolean>(false);
  const [currPage, setCurrPage] = useState<"Overview" | "Endpoint">("Overview");
  const [currEndpointIdx, setCurrEndpointIdx] = useState<number>(-1);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [currEndpoint, setCurrEndpoint] = useState<Endpoint>({
    link: "",
    method: "GET",
    title_description: "title_description place holder",
    main_description: "",
    tab: "",
    parameters: [],
    responses: [],
  });

  // Hooks
  const navigate = useNavigate();
  const auth = useAuth();
  const { logout } = auth!;

  useEffect(() => {
    setVersionUpdated(true);
  }, [endpoints, selectedFile]);

  useEffect(() => {
    const fetchApi = async () => {
      if (apiId === undefined) {
        return;
      }
      try {
        const data = await getApi(apiId);
        setApi(data);
        setName(data.name);
        setDescription(data.description);
        setSelectedTags(data.tags);
      } catch (error) {
        console.log("Error fetching data", error);
        toast.error("Error loading API data");
      }
    };
    fetchApi();
  }, [apiId, currEndpoint]);

  const submitApiOverlay = () => {
    try{
      if (apiId === undefined) {
        // create new api
        addApi({
          name,
          description,
          tags: selectedTags,
          pay_model:payModel,
          endpoints,
          version_name: versionName,
          version_description: versionDescription,
        })
        
      } else {
        // update existing api
      }
      toast.success("Success!");
      setIsVersionInfoOverlayOpen(false);
    }catch (error) {
      if (error instanceof Error && error.message === "Unauthorized") {
        logout();
        navigate("/login");
      }
    }
  };

  // Submit the API update to the backend
  const submitApi = async () => {
    console.log(versionUpdated);

    if (name === "") {
      toast.error("Name cannot be empty");
      return;
    } else if (description === "") {
      toast.error("Description cannot be empty");
      return;
    } else if (endpoints.length === 0) {
      toast.error("Please add at least one endpoint");
      return;
    }

    if (versionUpdated) {
      // create new api
      setIsVersionInfoOverlayOpen(true);
    } else {
      // update general info
    }

    // try {
    //   // Add newly created tags to the database
    //   for (const newTag of newTags) {
    //     if (selectedTags.includes(newTag)) {
    //       await addTag(newTag);
    //     }
    //   }

    //   // Edit existing API
    //   if (apiId) {
    //     await updateApi(
    //       name,
    //       description,
    //       selectedTags,
    //       "/testing/endpoint",
    //       apiId
    //     );
    //     if (selectedImageData) {
    //       const doc_id = await uploadImage(selectedImageData);
    //       apiAddIcon(apiId, doc_id);
    //     }
    //     if (selectedFile) {
    //       const doc_id = await uploadPDF(selectedFile);
    //       await uploadDocs(apiId, doc_id);
    //     }
    //     navigate(`/profile/my-apis/${apiId}`);

    //     // Add new API
    //   } else {
    //     const newId = await addApi(
    //       name,
    //       description,
    //       selectedTags,
    //       "/testing/endpoint"
    //     );
    //     if (selectedImageData) {
    //       const doc_id = await uploadImage(selectedImageData);
    //       apiAddIcon(newId, doc_id);
    //     }

    //     if (selectedFile) {
    //       const doc_id = await uploadPDF(selectedFile);
    //       await uploadDocs(newId, doc_id);
    //     }
    //     navigate(`/profile/my-apis/${newId}`);
    //   }

    //   toast.success("Success!");
    // } catch (error) {
    //   if (error instanceof Error && error.message === "Unauthorized") {
    //     logout();
    //     navigate("/login");
    //   }
    //   toast.error("Error updating API");
    // }
  };

  return (
    <div className="flex h-screen">
      {/* Main Content */}
      <div className="w-5/6 h-full p-6">
        {currPage === "Overview" && (
          <OverviewUpdateForm
            name={name}
            description={description}
            selectedTags={selectedTags}
            newTags={newTags}
            payModel={payModel}
            selectedImage={selectedImage}
            selectedImageData={selectedImageData}
            selectedFile={selectedFile}
            setName={setName}
            setPayModel={setPayModel}
            setDescription={setDescription}
            setSelectedTags={setSelectedTags}
            setNewTags={setNewTags}
            setSelectedImage={setSelectedImage}
            setSelectedImageData={setSelectedImageData}
            setSelectedFile={setSelectedFile}
          />
        )}
        {currPage === "Endpoint" && (
          <EndpointUpdateForm
            currEndpoint={currEndpoint}
            endpoints={endpoints}
            currEndpointIdx={currEndpointIdx}
            setCurrEndpoint={setCurrEndpoint}
            setEndpoints={setEndpoints}
            setCurrEndpointIdx={setCurrEndpointIdx}
          />
        )}
      </div>

      {(versionUpdated || apiId !== undefined) && (
        <VersionInfoOverlay
          isVersionInfoOverlayOpen={isVersionInfoOverlayOpen}
          versionName={versionName}
          versionDescription={versionDescription}
          setVersionName={setVersionName}
          setVersionDescription={setVersionDescription}
          setIsVersionInfoOverlayOpen={setIsVersionInfoOverlayOpen}
          onSubmit={submitApiOverlay}
        />
      )}

      {/* Sidebar */}
      <div className="w-1/6 bg-white border-l">
        <EndpointsSidebar
          currEndpoint={currEndpoint}
          currEndpointIdx={currEndpointIdx}
          endpoints={endpoints}
          currPage={currPage}
          setEndpoints={setEndpoints}
          setCurrPage={setCurrPage}
          setCurrEndpoint={setCurrEndpoint}
          setCurrEndpointIdx={setCurrEndpointIdx}
          submitApi={submitApi}
        />
      </div>
    </div>
  );
};

export default EditApiForm;
