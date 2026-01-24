import { Button } from "@/components/ui/button";
import React from "react";

interface PrimaryButtonProps {
  onClick?: () => void;
  children: React.ReactNode;
}

const PrimaryButton = ({ onClick, children }: PrimaryButtonProps) => (
  <Button 
    className="bg-purple-800 text-white text-lg px-6 py-2 rounded-md shadow hover:bg-purple-700"
    onClick={onClick}>
    {children}
  </Button>
);

export default PrimaryButton;