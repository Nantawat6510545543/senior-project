import React from "react";

const Navbar: React.FC = () => {
  return (
    <div>
      <nav className="fixed top-0 left-0 right-0 z-50 bg-purple-800 text-white px-6 py-4 flex items-center justify-between">
        <div className="text-2xl font-bold">SSL-MI-EEG</div>
      </nav>
      <div className="pt-16"></div>
    </div>
  );
};

export default Navbar;
