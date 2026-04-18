export function EmptyState() {
  return (
    <div className="flex flex-col items-center justify-center py-24 gap-3 text-slate-400">
      <span className="text-6xl">🛒</span>
      <p className="text-lg font-medium text-slate-500">Add items to your list</p>
      <p className="text-sm">Enter items and your ZIP code, then click Compare Prices.</p>
    </div>
  )
}
