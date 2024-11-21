import React, { useEffect, useState } from "react";
import EndpointsSidebar from "./EndPointsSideBar";
import { Endpoint } from "../types/backendTypes";
import OverviewUpdateForm from "./OverviewUpdateForm";
import EndpointUpdateForm from "./EndpointUpdateForm";
import {
  addApi,
  addNewVersion,
  addTag,
  apiAddIcon,
  getApi,
  updateServiceGlobal,
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
import UploadModal from "./UploadModal";

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
  const [generalInfoUpdated, setGeneralInfoUpdated] = useState<boolean>(false);
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
  const [createModal, setCreateModal] = useState<boolean>(false);


  // Hooks
  const navigate = useNavigate();
  const auth = useAuth();
  const { logout } = auth!;

  useEffect(() => {
    const fetchApi = async () => {
      if (apiId !== undefined) {
        try {
          const data = await getApi(apiId);
          setApi(data);
          setName(data.name);
          setDescription(data.description);
          setSelectedTags(data.tags);
          setPayModel(data.pay_model);
          setEndpoints(data.versions[0].endpoints);
        } catch (error) {
          toast.error("Error loading API data");
        }
      } else {
        setCreateModal(true);
      }
    };
    fetchApi();
  }, []);

  const handleCloseModal = () => {
    setCreateModal(false);
  };

  const submitApiOverlay = async () => {
    try {
      if (apiId === undefined) {
        // create new api
        const newId = await addApi({
          name,
          description,
          tags: selectedTags,
          pay_model: payModel,
          endpoints,
          version_name: versionName,
          version_description: versionDescription,
        });

        if (selectedImageData) {
          const doc_id = await uploadImage(selectedImageData);
          apiAddIcon(newId, doc_id);
        }
        if (selectedFile) {
          const doc_id = await uploadPDF(selectedFile);
          await uploadDocs(newId, doc_id, versionName);
        }
        navigate(`/profile/my-apis/${newId}`);
      } else {
        // update existing api
        for (const preVer of api!.versions) {
          if (preVer.version_name === versionName) {
            toast.error("Version name already exists");
            return;
          }
        }
        try {
          await addNewVersion(
            apiId,
            versionName,
            versionDescription,
            endpoints
          );
          if (selectedImageData) {
            const doc_id = await uploadImage(selectedImageData);
            apiAddIcon(apiId, doc_id);
          }
          if (selectedFile) {
            const doc_id = await uploadPDF(selectedFile);
            await uploadDocs(apiId, doc_id, versionName);
          }
          toast.success("Success!");
        } catch (error) {
          if (error instanceof Error && error.message === "PendingService") {
            toast.error(
              "Cannot create new version while service is pending approval"
            );
          }
        }
        setIsVersionInfoOverlayOpen(false);
        navigate(`/profile/my-apis/${apiId}`);
      }
    } catch (error) {
      if (error instanceof Error && error.message === "Unauthorized") {
        logout();
        navigate("/login");
      }
    }
  };

  // Submit the API update to the backend
  const submitApi = async () => {
    if (name === "") {
      toast.error("Name cannot be empty");
      return;
    } else if (name.length > 30) {
      toast.error("Name cannot be longer than 30 characters");
      return;
    } else if (description === "") {
      toast.error("Description cannot be empty");
      return;
    } else if (endpoints.length === 0) {
      toast.error("Please add at least one endpoint");
      return;
    }

    for (const newTag of newTags) {
      if (selectedTags.includes(newTag)) {
        await addTag(newTag);
      }
    }

    if (apiId === undefined) {
      // create new api
      setIsVersionInfoOverlayOpen(true);
    } else {
      // update
      if (selectedImageData) {
        const doc_id = await uploadImage(selectedImageData);
        apiAddIcon(apiId, doc_id);
      }
      if (generalInfoUpdated && versionUpdated) {
        updateServiceGlobal(name, description, selectedTags, payModel, apiId);
        setIsVersionInfoOverlayOpen(true);
      }
      if (versionUpdated) {
        // version specific update
        setIsVersionInfoOverlayOpen(true);
      }
      if (generalInfoUpdated) {
        // general info update
        updateServiceGlobal(name, description, selectedTags, payModel, apiId);
        toast.success("Success!");
        navigate(`/profile/my-apis/${apiId}`);
      }

      if (!versionUpdated && !generalInfoUpdated) {
        toast.error("No changes to update");
      }
    }
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
            setVersionUpdated={setVersionUpdated}
            setGeneralInfoUpdated={setGeneralInfoUpdated}
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
            setVersionUpdated={setVersionUpdated}
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
      {createModal && (
        <UploadModal
          isOpen={true}
          onRequestClose={handleCloseModal}
          onErrorReset={setCreateModal}
        />
      )}
    </div>
  );
};

export default EditApiForm;
