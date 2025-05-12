import Navbar from "@/components/Navbar";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Train from "./pages/Train";
import Predict from "./pages/Predict";
import Evaluate from "./pages/Evaluate";
import Compare from "./pages/Compare";

function App() {
  return (
    <Router>
      <Navbar />
      <div className="p-4">
        <Routes>
          <Route path="/train" element={<Train />} />
          <Route path="/predict" element={<Predict />} />
          <Route path="/evaluate" element={<Evaluate />} />
          <Route path="/compare" element={<Compare />} />
        </Routes>
      </div>
    </Router>
  );
}
export default App
