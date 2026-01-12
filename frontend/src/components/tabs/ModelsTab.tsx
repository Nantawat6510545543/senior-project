
import { useState } from "react";

import { SubHeader } from "@/components/Fonts";
import Combobox from "../ComboBox";

export default function ModelsTab() {
  const [model, setModel] = useState("");

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
      <SubHeader>Model</SubHeader>
      <Combobox
        options={[
          { value: "CNNLSTMDense", label: "CNNLSTMDense" },
          { value: "EEGNet", label: "EEGNet" },
          { value: "EEGNetMultiOutput", label: "EEGNetMultiOutput" },
          { value: "SimpleNN", label: "SimpleNN" },
        ]}
        value={model}
        onChange={setModel}
      />
    </div>
  );
}


