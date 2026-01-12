import { SubHeader } from "@/components/Fonts"
import PurpleCheckbox from "@/components/PurpleCheckbox"
import { useState } from "react";
import Combobox from "../ComboBox";

export default function EvokedDisplayTab() {
  const [gfp, setGfp] = useState(""); // "" means no selection
  const [scaleMode, setScaleMode] = useState("");

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div>
          <SubHeader>GFP</SubHeader>
          <Combobox
            options={[
              { value: "False", label: "False" },
              { value: "True", label: "True" },
              { value: "Only", label: "Only" },
            ]}
            value={gfp}
            onChange={setGfp}
          />
        </div>
        <div>
          <SubHeader>Scale Mode</SubHeader>
          <Combobox
            options={[
              { value: "per-plot", label: "per-plot" },
              { value: "uniform-grid", label: "uniform-grid" },
            ]}
            value={scaleMode}
            onChange={setScaleMode}
          />
        </div>
        <div>
          <SubHeader>Average Line</SubHeader>
          <PurpleCheckbox />
        </div>
        <div>
          <SubHeader>Spatial Colors</SubHeader>
          <PurpleCheckbox />
        </div>
      </div>
    </div>
  );
}
