type Props = {
  data: any[]
}

export default function PurpleTable({ data }: Props) {
  if (!data?.length) {
    return (
      <div className="rounded-xl border border-purple-200 bg-purple-50 p-6 text-purple-800">
        No data available
      </div>
    )
  }

  const columns = Object.keys(data[0])

  return (
    <div className="w-full overflow-x-auto rounded-xl border border-purple-200 bg-purple-50 shadow-sm">
      <table className="w-full text-base">

        {/* Header */}
        <thead className="bg-purple-800 text-white">
          <tr>
            {columns.map((col) => (
              <th
                key={col}
                className="px-4 py-3 text-left font-semibold"
              >
                {col}
              </th>
            ))}
          </tr>
        </thead>

        {/* Body */}
        <tbody className="text-purple-900">
          {data.map((row, i) => (
            <tr
              key={i}
              className="border-b border-purple-200 hover:bg-purple-100 transition"
            >
              {columns.map((col) => {
                const value = row[col]

                return (
                  <td key={col} className="px-4 py-2 whitespace-nowrap">
                  {value === null || value === undefined
                    ? "—"
                    : typeof value === "number"
                    ? Number.isInteger(value)
                      ? value.toLocaleString()
                      : value.toFixed(3)
                    : Array.isArray(value)
                    ? `[${value.join(", ")}]`
                    : value.toString()}
                  </td>
                )
              })}
            </tr>
          ))}
        </tbody>

      </table>
    </div>
  )
}