import { useState } from "react";
import { Label } from "@/components/ui/label";
import Combobox from "@/components/ComboBox";
import FileUploadButton from "@/components/FileUploadButton";
import { predictModel } from "@/api/api";
import PrimaryButton from "@/components/PrimaryButton";

const model_options = [
  { value: "Mixnet", label: "MixNet" }
];

const Predict = () => {
  const [selectedFile, setFile] = useState<File | null>(null);
  const [selectedModel, setSelectedModel] = useState<string>("");
  const [prediction, setPrediction] = useState({
    class: "Deep Sleep",
    confidence: 92.3,
  });

  const handlePredict = async () => {
    if (selectedFile) {
      return await predictModel({
        file: selectedFile,
        model_name: selectedModel,
      });
    } else {
      alert("File is missing!")
    }
  };

  return (
    <div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-start">
        <div className="space-y-6">
          <div className="space-y-2">
            <Label className="text-purple-800 text-lg mb-2 block">Select data</Label>
            <FileUploadButton fileName={selectedFile?.name || ""} onFileChange={setFile} />
          </div>

          <div className="space-y-2">
            <Label className="text-purple-800 text-lg mb-2 block">Select model</Label>
            <Combobox options={model_options} value={selectedModel} onChange={setSelectedModel} />
          </div>

          <PrimaryButton onClick={handlePredict}>
            Predict
          </PrimaryButton>
        </div>

        <div className="text-purple-900 text-lg space-y-2">
          <h2 className="font-semibold text-xl">Prediction:</h2>
          <p><strong>Class:</strong> {prediction.class}</p>
          <p><strong>Confidence:</strong> {prediction.confidence}%</p>
        </div>
      </div>
    </div>
  );
};

export default Predict;
