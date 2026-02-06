import { useEffect, useState } from "react"
import IntegerInput from "@/components/IntegerInput"
import DecimalInput from "@/components/DecimalInput"
import { Input } from "@/components/ui/input"
import PurpleCheckbox from "@/components/PurpleCheckbox"
import { SubHeader } from "@/components/Fonts"
import Combobox from "../ComboBox"
import useSessionPatch from "@/hooks/useSessionPatch"
import useLoadSession from "@/hooks/useLoadSession"
import type { SchemaEndpoints } from "@/hooks/useSchema"

function resolveFieldType(field: any) {
  if (field.anyOf) {
    const types = field.anyOf.map((t: any) => t.type)
    if (types.includes("number")) return "number"
    if (types.includes("string")) return "string"
  }
  return field.type
}

function getSchemaFieldsByGroup(schema: any, groups: string[]) {
  if (!schema?.properties) return []
  return Object.keys(schema.properties).filter(
    (name) => groups.includes(schema.properties[name].group)
  )
}

export default function SchemaFieldGrid({
  schema,
  groups,
  sessionId,
  endpoint,
}: {
  schema: any
  groups: string[]
  sessionId: string
  endpoint: SchemaEndpoints
}) {

  const fields = getSchemaFieldsByGroup(schema, groups)

  // STRING-BASED UI STATE
  const sessionValues = useLoadSession(sessionId, endpoint)
  const [values, setValues] = useState<Record<string, any>>({})
  useSessionPatch(sessionId, endpoint, values)

  const setField = (name: string, value: any) => {
    setValues(prev => ({ ...prev, [name]: value }))
  }

  useEffect(() => {
    if (sessionValues) {
      setValues(sessionValues)
    }
  }, [sessionValues])

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
      {fields.map((name) => {
        const field = schema.properties[name]
        const type = resolveFieldType(field)

        return (
          <div key={name}>
            <SubHeader>{field.title ?? name}</SubHeader>

            {type === "boolean" && (
              <PurpleCheckbox
                checked={values[name] ?? field.default ?? false}
                onChange={(v) => setField(name, v)}
              />
            )}

            {type === "integer" && (
              <IntegerInput
                placeholder={String(field.default ?? "")}
                value={values[name]}
                onChange={(v) => setField(name, v)}
              />
            )}

            {type === "number" && (
              <DecimalInput
                placeholder={String(field.default ?? "")}
                value={values[name]}
                onChange={(v) => setField(name, v)}
              />
            )}

            {type === "string" && (
              <Input
                value={values[name] ?? field.default ?? ""}
                onChange={(e) => setField(name, e.target.value)}
              />
            )}

            {type === "array" && (
              <Combobox
                options={field.options.map((v: string) => ({ value: v, label: v }))}
                value={values[name] ?? field.default}
                onChange={(v) => setField(name, v)}
              />
            )}
          </div>
        )
      })}
    </div>
  )
}
