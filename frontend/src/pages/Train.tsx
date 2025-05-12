import { Combobox } from "@/components/ComboBox";

const frameworks = [
  { value: "next.js", label: "Next.js" },
  { value: "sveltekit", label: "SvelteKit" },
  { value: "nuxt.js", label: "Nuxt.js" },
  { value: "remix", label: "Remix" },
  { value: "astro", label: "Astro" },
];

const Train = () => {
  return (
    <div>
      <h1>Train Page</h1>
      <Combobox options={frameworks} />
    </div>
  );
};

export default Train;