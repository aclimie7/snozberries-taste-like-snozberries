import { useStore } from '../../store'
import type { ShoppingItem } from '../../types/shopping-list'

export function ItemRow({ item }: { item: ShoppingItem }) {
  const removeItem = useStore((s) => s.removeItem)
  const updateQuantity = useStore((s) => s.updateQuantity)
  const updateName = useStore((s) => s.updateName)

  return (
    <div className="flex items-center gap-2 py-1">
      <input
        className="flex-1 border border-slate-200 rounded px-2 py-1 text-sm focus:outline-none focus:ring-1 focus:ring-blue-400"
        value={item.name}
        onChange={(e) => updateName(item.id, e.target.value)}
      />
      <input
        type="number"
        min={1}
        max={99}
        className="w-14 border border-slate-200 rounded px-2 py-1 text-sm text-center focus:outline-none focus:ring-1 focus:ring-blue-400"
        value={item.quantity}
        onChange={(e) => updateQuantity(item.id, Number(e.target.value))}
      />
      <button
        onClick={() => removeItem(item.id)}
        className="text-slate-400 hover:text-red-500 text-lg leading-none px-1"
        aria-label="Remove item"
      >
        ×
      </button>
    </div>
  )
}
