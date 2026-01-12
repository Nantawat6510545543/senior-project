import { Button } from "@/components/ui/button"

interface OptionButtonsProps {
  options: string[]
  value: string
  onChange: (value: string) => void
}

export default function OptionButtons({
  options,
  value,
  onChange,
}: OptionButtonsProps) {
  return (
    <div className="flex gap-2 flex-wrap">
    {options.map((opt) => (
        <Button
        key={opt}
        variant={value === opt ? undefined : "outline"}
        className={
            value === opt
            ? "bg-purple-800 text-lg text-white hover:bg-purple-700"
            : "border-purple-800 text-lg text-purple-800"
        }
        onClick={() => onChange(opt)}
        >
        {opt}
        </Button>
    ))}
    </div>
  )
}