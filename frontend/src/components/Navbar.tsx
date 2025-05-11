import React from "react";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";

const Navbar: React.FC = () => {
  return (
    <nav className="flex items-center justify-between px-6 py-4 border-b">
      <div className="text-xl font-semibold">SSL-MI-EEG</div>
      <div className="flex space-x-4">
        <Link to="/train"><Button variant="outline">Train</Button></Link>
        <Link to="/predict"><Button variant="outline">Predict</Button></Link>
        <Link to="/evaluate"><Button variant="outline">Evaluate</Button></Link>
        <Link to="/compare"><Button variant="outline">Compare</Button></Link>
      </div>
    </nav>
  );
};

export default Navbar;