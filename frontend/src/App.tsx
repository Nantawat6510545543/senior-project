import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";

import EEGUI from "./pages/EEGUI";
import Navbar from "@/components/Navbar";
import SessionForm from "./components/forms/SessionForm";

function App() {
  return (
    <div className="min-h-screen bg-purple-100 p-6 rounded-none">
      <Router>
        <Navbar />
        <div className="p-4">
          <Routes>
            <Route path="/" element={<Navigate replace to="/eegui" />} />
            <Route path="/eegui" element={
              <SessionForm><EEGUI /></SessionForm>}
            />
          </Routes>
        </div>
      </Router>
    </div>
  );
}

export default App
