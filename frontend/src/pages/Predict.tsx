import { useState } from "react";
import { Label } from "@/components/ui/label";
import { Combobox } from "@/components/ComboBox";
import FileUploadButton from "@/components/FileUploadButton";
import ApiButton from "@/components/PrimaryButton";

const model_options = [
  { value: "Mixnet", label: "MixNet" }
]

const Predict = () => {
  const [fileName, setFileName] = useState("");
  const [selectedModel, setSelectedModel] = useState("");
  const [prediction, setPrediction] = useState({
    class: "Deep Sleep",
    confidence: 92.3,
  });

  const handleFileChange = (file: File) => {
    setFileName(file.name);
  };

  const handlePredict = () => {
    console.log("Predicting with file:", fileName);
  }

  return (
    <div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-start">
        <div className="space-y-6">
          <div className="space-y-2">
            <Label className="text-purple-800 text-lg mb-2 block">Select data</Label>
            <FileUploadButton fileName={fileName} onFileChange={handleFileChange} />
          </div>

          <div className="space-y-2">
            <Label className="text-purple-800">Select model</Label>
            <Combobox options={model_options} value={selectedModel} onChange={setSelectedModel}/>
          </div>

          <ApiButton onClickApi={handlePredict} label="Predict" />
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