import { useState } from "react"
import IntegerInput from "@/components/IntegerInput"
import DecimalInput from "@/components/DecimalInput"
import { Input } from "@/components/ui/input"
import PurpleCheckbox from "@/components/PurpleCheckbox"
import { SubHeader } from "@/components/Fonts"
import Combobox from "../ComboBox"

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
}: {
  schema: any
  groups: string[]
}) {
  const fields = getSchemaFieldsByGroup(schema, groups)

  // STRING-BASED UI STATE
  const [values, setValues] = useState<Record<string, any>>({})

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
                onChange={(v) =>
                  setValues((prev) => ({ ...prev, [name]: v }))
                }
              />
            )}

            {type === "integer" && (
              <IntegerInput
                placeholder={String(field.default ?? "")}
                value={values[name]}
                onChange={(v) =>
                  setValues((prev) => ({ ...prev, [name]: v }))
                }
              />
            )}

            {type === "number" && (
              <DecimalInput
                placeholder={String(field.default ?? "")}
                value={values[name]}
                onChange={(v) =>
                  setValues((prev) => ({ ...prev, [name]: v }))
                }
              />
            )}

            {type === "string" && (
              <Input
                defaultValue={field.default}
                onChange={(e) =>
                  setValues((prev) => ({
                    ...prev,
                    [name]: e.target.value,
                  }))
                }
              />
            )}

            {type === "array" && (
              <Combobox
                options={field.options.map((v: string) => ({ value: v, label: v }))}
                value={values[name] ?? field.default}
                onChange={(v) =>
                  setValues((prev) => ({ ...prev, [name]: v }))
                }
              />
            )}
          </div>
        )
      })}
    </div>
  )
}
