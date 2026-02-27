import { getSubjects } from "@/api/api";
import { useEffect, useState } from "react"


export default function useSubjectOption() {
  const [subjectOptions, setSubjectOptions] = useState<
    { value: string; label: string }[]
  >([])

  useEffect(() => {
    getSubjects()
      .then((subjects) =>
        setSubjectOptions(subjects.map((s) => ({ value: s, label: s })))
      )
      .catch(console.error)
  }, [])

  return subjectOptions
}
