import { ReplyDetail } from "../types/miscTypes";

interface ReplyDetailCardProps {
  review: ReplyDetail;
}

const ReplyDetailCard: React.FC<ReplyDetailCardProps> = ({ review }) => {
  const bgColor50 = "bg-yellow-50";
  const borderColor300 = "border-yellow-300";
  const textColor800 = "text-gray-800";
  const textColor500 = "text-gray-700";
  return (
    <div
      className={`p-3 bg-white border-2 ${borderColor300} rounded-lg`}
    >
      <div className={`flex items-center justify-between`}>
        <h2 className={`text-lg font-bold items-center justify-center ${textColor800}`}>
          {review.reviewerName}
        </h2>
      </div>
      <div className={`border ${borderColor300} w-full my-5`}></div>
      <div
        className={` ${bgColor50}  ${textColor500} font-semibold rounded-lg py-3 px-3`}
      >
        {review.comment}
      </div>
    </div>
  );
};

export default ReplyDetailCard;
