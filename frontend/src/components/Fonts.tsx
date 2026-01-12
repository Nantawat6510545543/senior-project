export function Header({ children }: { children: React.ReactNode }) {
  return (
    <div className="text-xl font-semibold text-purple-900">
      {children}
    </div>
  )
}

export function SubHeader({ children }: { children: React.ReactNode }) {
  return (
    <div className="text-lg font-medium text-purple-900 pb-1">
      {children}
    </div>
  )
}