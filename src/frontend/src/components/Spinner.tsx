import ClipLoader from "react-spinners/PacmanLoader";
import { FC } from "react";

const override = {
  display: "block",
  margin: "100px auto",
};

interface SpinnerProps {
  loading: boolean;
}

const Spinner: FC<SpinnerProps> = ({ loading }) => {
  return (
    <ClipLoader
      color="#4338ca"
      loading={loading}
      cssOverride={override}
      size={50}
    />
  );
};
export default Spinner;
