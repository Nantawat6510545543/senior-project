import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { UploadCloud } from "lucide-react";
import { Combobox } from "@/components/ComboBox";

const model_options = [
  { value: "Mixnet", label: "MixNet" }
]

const Predict = () => {
  const [fileName, setFileName] = useState("");
  const [prediction, setPrediction] = useState({
    class: "Deep Sleep",
    confidence: 92.3,
  });

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.length) {
      setFileName(e.target.files[0].name);
    }
  };

  return (
    <div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-start">
        <div className="space-y-6">
          <div className="space-y-2">
            <Label className="text-purple-800">Select data</Label>
            <input type="file" id="file-upload" className="hidden" onChange={handleFileUpload} />
            <label htmlFor="file-upload">
              <Button variant="outline" className="w-full bg-purple-200 text-purple-900 border border-purple-300 shadow-md">
                <UploadCloud className="mr-2 h-5 w-5" /> Upload {fileName && `(${fileName})`}
              </Button>
            </label>
          </div>

          <div className="space-y-2">
            <Label className="text-purple-800">Select model</Label>
            <Combobox options={model_options} />
          </div>

          <Button className="bg-purple-800 text-white px-6 py-2 rounded-md shadow hover:bg-purple-700">
            Predict
          </Button>
        </div>

        <div className="text-purple-900 text-lg space-y-2">
          <h2 className="font-semibold text-xl">Prediction:</h2>
          <p><strong>Class:</strong> {prediction.class}</p>
          <p><strong>Confidence:</strong> {prediction.confidence}%</p>
        </div>
      </div>
    </div>
  );
}

export default Predict;