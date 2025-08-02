import React from "react";

interface Props {
  completed: number;
  total: number;
}

const GoalProgress: React.FC<Props> = ({ completed, total }) => {
  const percentage = Math.round((completed / total) * 100);

  return (
    <div className="mt-2">
      <h3 className="text-sm text-gray-600 font-medium mb-1">Goal Completion</h3>
      <div className="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
        <div
          className={`h-4 rounded-full transition-all duration-300 ${
            percentage < 50
              ? "bg-red-500"
              : percentage < 80
              ? "bg-yellow-500"
              : "bg-green-500"
          }`}
          style={{ width: `${percentage}%` }}
        />
      </div>
      <p className="text-xs mt-1 text-gray-500">
        {completed} of {total} goals completed ({percentage}%)
      </p>
    </div>
  );
};

export default GoalProgress;