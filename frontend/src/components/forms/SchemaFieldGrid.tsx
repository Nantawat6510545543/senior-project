"use client"

import IntegerInput from "@/components/IntegerInput"
import DecimalInput from "@/components/DecimalInput"
import { Input } from "@/components/ui/input"
import PurpleCheckbox from "@/components/PurpleCheckbox"
import { SubHeader } from "@/components/Fonts"
import Combobox from "../ComboBox"

import { Controller, useFormContext } from "react-hook-form"

import type { SchemaEndpoints } from "@/hooks/useSchema"
import type { SessionFormSchema } from "@/api/types"


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
// TODO render all default varaiable field at once
export default function SchemaFieldGrid({ schema, groups, endpoint }: {
  schema: any
  groups: string[]
  endpoint: SchemaEndpoints
}) {

  const { control } = useFormContext<SessionFormSchema>()
  const fields = getSchemaFieldsByGroup(schema, groups)

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
      {fields.map((name) => {
        const field = schema.properties[name]
        const fieldName = `${endpoint}.${name}`

        return (
          <div key={name}>
            <SubHeader>{field.title ?? name}</SubHeader>

            {field.ui === "checkbox" && (
              <Controller
                name={fieldName}
                control={control}
                defaultValue={field.default ?? false}
                render={({ field }) => (
                  <PurpleCheckbox
                    checked={field.value}
                    onChange={field.onChange}
                  />
                )}
              />
            )}

            {field.ui === "integer" && (
              <Controller
                name={fieldName}
                control={control}
                defaultValue={field.default ?? null}
                render={({ field }) => (
                  <IntegerInput
                    value={field.value}
                    placeholder={resolvePlaceholder(field)}
                    onChange={field.onChange}
                  />
                )}
              />
            )}

            {field.ui === "number" && (
              <Controller
                name={fieldName}
                control={control}
                defaultValue={field.default ?? null}
                render={({ field }) => (
                  <DecimalInput
                    value={field.value}
                    placeholder={resolvePlaceholder(field)}
                    onChange={field.onChange}
                  />
                )}
              />
            )}

            {field.ui === "text" && (
              <Controller
                name={fieldName}
                control={control}
                defaultValue={field.default ?? ""}
                render={({ field }) => (
                  <Input
                    {...field}
                    placeholder={resolvePlaceholder(field)}
                  />
                )}
              />
            )}

            {field.ui === "list" && (
              <Controller
                name={fieldName}
                control={control}
                defaultValue={field.default}
                render={({ field: rhfField }) => (
                  <Combobox
                    options={field.options.map((v: string) => ({
                      value: v,
                      label: v,
                    }))}
                    value={rhfField.value}
                    onChange={rhfField.onChange}
                  />
                )}
              />
            )}

            {field.ui === "range" && (
              <div className="flex gap-2">
                <Controller
                  name={`${fieldName}.min`}
                  control={control}
                  render={({ field }) => (
                    <DecimalInput
                      value={field.value ?? ""}
                      placeholder="min"
                      onChange={field.onChange}
                    />
                  )}
                />

                <Controller
                  name={`${fieldName}.max`}
                  control={control}
                  render={({ field }) => (
                    <DecimalInput
                      value={field.value ?? ""}
                      placeholder="max"
                      onChange={field.onChange}
                    />
                  )}
                />
              </div>
            )}
          </div>
        )
      })}
    </div>
  )
}