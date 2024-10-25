import { useOutletContext } from 'react-router-dom';
import ApiListings from '../components/ApiListings';

interface OutletContext {
  selectedTags: string[];
}

const ApisPage: React.FC = () => {
  const { selectedTags } = useOutletContext<OutletContext>();
  return (
      <ApiListings isMyAPis={false} selectedTags={selectedTags}/>
  );
};
export default ApisPage;
