import { useStore } from '../../store'
import { useComparison } from '../../hooks/useComparison'
import { AddItemForm } from './AddItemForm'
import { ItemRow } from './ItemRow'

export function ShoppingListPanel() {
  const items = useStore((s) => s.items)
  const zipCode = useStore((s) => s.zipCode)
  const setZipCode = useStore((s) => s.setZipCode)
  const clearItems = useStore((s) => s.clearItems)
  const { runComparison, loading, canCompare } = useComparison()

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-4 space-y-4">
      <h2 className="font-semibold text-slate-800 text-base">Shopping List</h2>

      <div>
        <label className="block text-xs font-medium text-slate-500 mb-1">ZIP Code</label>
        <input
          className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="e.g. 90210"
          value={zipCode}
          maxLength={5}
          onChange={(e) => setZipCode(e.target.value.replace(/\D/g, ''))}
        />
      </div>

      <div>
        <label className="block text-xs font-medium text-slate-500 mb-1">Items</label>
        <div className="space-y-1 mb-2 max-h-64 overflow-y-auto">
          {items.map((item) => (
            <ItemRow key={item.id} item={item} />
          ))}
          {items.length === 0 && (
            <p className="text-slate-400 text-xs py-2">No items yet.</p>
          )}
        </div>
        <AddItemForm />
        {items.length > 0 && (
          <button
            onClick={clearItems}
            className="text-xs text-slate-400 hover:text-slate-600 mt-1"
          >
            Clear all
          </button>
        )}
      </div>

      <button
        onClick={runComparison}
        disabled={!canCompare || loading}
        className="w-full bg-blue-600 text-white rounded-lg py-2.5 text-sm font-semibold hover:bg-blue-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
      >
        {loading ? 'Searching...' : 'Compare Prices'}
      </button>

      {!canCompare && (
        <p className="text-xs text-slate-400 text-center">
          Add items and a 5-digit ZIP to compare
        </p>
      )}
    </div>
  )
}
