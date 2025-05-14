import { Button } from "@/components/ui/button";
import React from "react";

interface ApiButtonProps {
  onClickApi: () => void;
  label?: string;
}

const ApiButton: React.FC<ApiButtonProps> = ({ onClickApi, label = "Submit" }) => {
  const handleClick = async () => {
    try {
      const data = await onClickApi();
      console.log("Response:", data);
    } catch (error) {
      console.error("API call failed:", error);
    }
  };

  return (
    <Button
      className={"bg-purple-800 text-white px-6 py-2 rounded-md shadow hover:bg-purple-700"}
      onClick={handleClick}
    >
      {label}
    </Button>
  );
};

export default ApiButton;
