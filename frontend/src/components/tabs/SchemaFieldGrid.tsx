import { useEffect } from "react"
import IntegerInput from "@/components/IntegerInput"
import DecimalInput from "@/components/DecimalInput"
import { Input } from "@/components/ui/input"
import PurpleCheckbox from "@/components/PurpleCheckbox"
import { SubHeader } from "@/components/Fonts"
import Combobox from "../ComboBox"
import useSessionPatch from "@/hooks/useSessionPatch"
import useLoadSession from "@/hooks/useLoadSession"
import type { SchemaEndpoints } from "@/hooks/useSchema"

import { useForm, Controller, useWatch } from "react-hook-form"


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
  const { control, reset } = useForm({
    defaultValues: sessionValues || {}
  })

  const values = useWatch({ control })
  useSessionPatch(sessionId, endpoint, values)

  useEffect(() => {
    if (sessionValues) {
      reset(sessionValues)
    }
  }, [sessionValues, reset])

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
      {fields.map((name) => {
        const field = schema.properties[name]

        return (
          <div key={name}>
            <SubHeader>{field.title ?? name}</SubHeader>

            {field.ui === "checkbox" && (
              <Controller
                name={name}
                control={control}
                defaultValue={field.default ?? false}
                render={({ field: rhfField }) => (
                  <PurpleCheckbox
                    checked={rhfField.value}
                    onChange={rhfField.onChange}
                  />
                )}
              />
            )}

            {field.ui === "integer" && (
              <Controller
                name={name}
                control={control}
                defaultValue={field.default ?? ""}
                render={({ field: rhfField }) => (
                  <IntegerInput
                    value={rhfField.value ?? ""}
                    placeholder={resolvePlaceholder(field)}
                    onChange={rhfField.onChange}
                  />
                )}
              />
            )}

            {field.ui === "number" && (
              <Controller
                name={name}
                control={control}
                defaultValue={field.default ?? ""}
                render={({ field: rhfField }) => (
                  <DecimalInput
                    value={rhfField.value ?? ""}
                    placeholder={resolvePlaceholder(field)}
                    onChange={rhfField.onChange}
                  />
                )}
              />
            )}

            {field.ui === "text" && (
              <Controller
                name={name}
                control={control}
                defaultValue={field.default ?? ""}
                render={({ field: rhfField }) => (
                  <Input
                    {...rhfField}
                    placeholder={resolvePlaceholder(field)}
                  />
                )}
              />
            )}

            {field.ui === "list" && (
              <Controller
                name={name}
                control={control}
                defaultValue={field.default}
                render={({ field: rhfField }) => (
                  <Combobox
                    options={field.options.map((v: string) => ({ value: v, label: v }))}
                    value={rhfField.value}
                    onChange={rhfField.onChange}
                  />
                )}
              />
            )}
          </div>
        )
      })}
    </div>
  )
}
