import ApiListings from '../components/ApiListings';

const ApisPage = () => {
  return (
    <section className='bg-gradient-to-b from-blue-50 to-white py-6'>
      <ApiListings isMyAPis={false}/>
    </section>
  );
};
export default ApisPage;
