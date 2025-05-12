import Navbar from "@/components/Navbar";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Train from "./pages/Train";
import Predict from "./pages/Predict";
import Evaluate from "./pages/Evaluate";
import Compare from "./pages/Compare";

function App() {
  return (
    <div className="min-h-screen bg-purple-100 p-6">
      <Router>
        <Navbar />
        <div className="p-4">
          <Routes>
            <Route path="/" element={<Navigate replace to="/train" />} />
            <Route path="/train" element={<Train />} />
            <Route path="/predict" element={<Predict />} />
            <Route path="/evaluate" element={<Evaluate />} />
            <Route path="/compare" element={<Compare />} />
          </Routes>
        </div>
      </Router>
    </div>
  );
}
export default App
