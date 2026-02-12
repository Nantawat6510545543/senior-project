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


function resolveValue(field: any, value: any) {
  if (value !== undefined && value !== null) return value
  if (field.default !== undefined && field.default !== null) return field.default
  return ""
}

function resolvePlaceholder(field: any) {
  if (field.default !== undefined && field.default !== null) return undefined
  return field.placeholder ?? ""
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

        return (
          <div key={name}>
            <SubHeader>{field.title ?? name}</SubHeader>

            {field.ui === "checkbox" && (
              <PurpleCheckbox
                checked={Boolean(values[name] ?? field.default)}
                onChange={(v) => setField(name, v)}
              />
            )}

            {field.ui === "integer" && (
              <IntegerInput
                value={resolveValue(field, values[name])}
                placeholder={resolvePlaceholder(field)}
                onChange={(v) => setField(name, v)}
              />
            )}

            {field.ui === "number" && (
              <DecimalInput
                value={resolveValue(field, values[name])}
                placeholder={resolvePlaceholder(field)}
                onChange={(v) => setField(name, v)}
              />
            )}

            {field.ui === "text" && (
              <Input
                value={resolveValue(field, values[name])}
                placeholder={resolvePlaceholder(field)}
                onChange={(e) => setField(name, e.target.value)}
              />
            )}

            {field.ui === "list" && (
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
