import { Input } from "@/components/ui/input"
import NumberInput from "@/components/NumberInput"
import { SubHeader } from "@/components/Fonts"
import PurpleCheckbox from "@/components/PurpleCheckbox"

export default function FilteringCleaningTab() {
  return (
    <div>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {[
          "l_freq",
          "h_freq",
          "notch",
          "resample_fs",
          "uv_min",
          "uv_max",
          "clean_flatline_sec",
          "clean_hf_noise_sd_max",
        ].map((f) => (
          <div key={f}>
            <SubHeader>{f}</SubHeader>
            <NumberInput />
          </div>
        ))}
      </div>

      <div className="mt-4">
        <SubHeader>Channels</SubHeader>
        <Input defaultValue="69-76,81-83,88,89" />
      </div>

      <div className="flex gap-6 mt-4">
        {["Combine channels", "Show bad", "ASR remove only"].map((t) => (
          <div key={t} className="flex items-center gap-2">
            <PurpleCheckbox />
            <SubHeader>{t}</SubHeader>
          </div>
        ))}
      </div>
    </div>
  )
}
