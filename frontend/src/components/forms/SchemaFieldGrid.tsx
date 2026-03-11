"use client"

import IntegerInput from "@/components/IntegerInput"
import DecimalInput from "@/components/DecimalInput"
import PurpleCheckbox from "@/components/PurpleCheckbox"
import Combobox from "@/components/ComboBox"
import { Input } from "@/components/ui/input"
import { SubHeader } from "@/components/Fonts"

import type { SchemaEndpoints } from "@/hooks/useSchema"

function getSchemaFieldsByGroup(schema: any, groups: string[]) {
  if (!schema?.properties) return []

  return Object.keys(schema.properties).filter(
    (name) => groups.includes(schema.properties[name].group)
  )
}

export default function SchemaFieldGrid({
  schema,
  groups,
  endpoint,
}: {
  schema: any
  groups: string[]
  endpoint: SchemaEndpoints
}) {
  const fields = getSchemaFieldsByGroup(schema, groups)

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
      {fields.map((name) => {
        const schemaField = schema.properties[name]
        const fieldName = `${endpoint}.${name}`

        return (
          <div key={name}>
            <SubHeader>{schemaField.title ?? name}</SubHeader>

            {schemaField.ui === "checkbox" && (
              <PurpleCheckbox
                name={fieldName}
                defaultValue={schemaField.default}
              />
            )}

            {schemaField.ui === "integer" && (
              <IntegerInput
                name={fieldName}
                placeholder={schemaField.placeholder}
                defaultValue={schemaField.default}
              />
            )}

            {schemaField.ui === "number" && (
              <DecimalInput
                name={fieldName}
                placeholder={schemaField.placeholder}
                defaultValue={schemaField.default}
              />
            )}

            {schemaField.ui === "text" && (
              <Input
                name={fieldName}
                placeholder={schemaField.placeholder}
                defaultValue={schemaField.default}
              />
            )}

            {schemaField.ui === "list" && (
              <Combobox
                name={fieldName}
                options={(schemaField.options ?? []).map((v: string) => ({
                  value: v,
                  label: v,
                }))}
                placeholder={schemaField.placeholder}
                defaultValue={schemaField.default}
              />
            )}

            {schemaField.ui === "range" && (
              <div className="flex gap-2">
                <DecimalInput
                  name={`${fieldName}.min`}
                  placeholder="min"
                  defaultValue={schemaField.default?.min}
                />

                <DecimalInput
                  name={`${fieldName}.max`}
                  placeholder="max"
                  defaultValue={schemaField.default?.max}
                />
              </div>
            )}
          </div>
        )
      })}
    </div>
  )
}