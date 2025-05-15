import { useRef } from "react";
import { UploadCloud } from "lucide-react";
import { Button } from "@/components/ui/button";

interface FileUploadButtonProps {
  fileName: string | null;
  onFileChange: (file: File) => void;
}

export default function FileUploadButton({ fileName, onFileChange }: FileUploadButtonProps) {
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      onFileChange(file); // Pass the file to the parent component
    }
  };

  return (
    <div className="grid w-full max-w-sm items-center gap-1.5">
      <input
        type="file"
        id="picture"
        ref={inputRef}
        className="hidden"
        onChange={handleFileChange}
      />
      <Button
        variant="outline"
        className="w-full bg-purple-200 text-purple-900 border border-purple-300 shadow-md"
        onClick={() => inputRef.current?.click()}
      >
        <UploadCloud className="mr-2 h-5 w-5" />
        {fileName || "Upload Picture"}
      </Button>
    </div>
  );
}
