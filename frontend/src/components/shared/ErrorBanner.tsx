export function ErrorBanner({ message, warnings = [] }: { message: string; warnings?: string[] }) {
  return (
    <div className="bg-red-50 border border-red-200 text-red-800 rounded-lg p-4 space-y-1">
      <p className="font-medium">Error: {message}</p>
      {warnings.map((w, i) => (
        <p key={i} className="text-sm text-red-600">{w}</p>
      ))}
    </div>
  )
}
