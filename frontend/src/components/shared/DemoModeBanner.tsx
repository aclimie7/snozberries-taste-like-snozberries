export function DemoModeBanner() {
  return (
    <div className="bg-amber-50 border border-amber-200 text-amber-800 text-sm px-4 py-2 rounded-lg flex items-center gap-2">
      <span>⚠️</span>
      <span>
        <strong>Demo mode</strong> — showing sample data. Add API keys in <code className="bg-amber-100 px-1 rounded">.env</code> for live prices.
      </span>
    </div>
  )
}
