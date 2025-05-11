import Navbar from "@/components/Navbar"; // Make sure path is correct
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

function App() {
  return (
    <Router>
      <Navbar />
      <div className="p-4">
        <Routes>
          <Route path="/train" element={<div>Train Page</div>} />
          <Route path="/predict" element={<div>Predict Page</div>} />
          <Route path="/evaluate" element={<div>Evaluate Page</div>} />
          <Route path="/compare" element={<div>Compare Page</div>} />
          <Route path="/" element={<div>Home</div>} />
        </Routes>
      </div>
    </Router>
  );
}
export default App
