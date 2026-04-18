import type { ItemComparison } from '../../types/product'
import { StoreColumn } from './StoreColumn'

export function ItemComparisonCard({ item }: { item: ItemComparison }) {
  const bestStore = item.recommended?.store ?? null

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-4 space-y-3">
      <div className="flex items-center justify-between">
        <h3 className="font-semibold text-slate-800 capitalize">
          {item.query}
          {item.quantity > 1 && <span className="text-slate-400 font-normal text-sm ml-1">×{item.quantity}</span>}
        </h3>
        {item.recommended && (
          <div className="text-xs text-slate-500 bg-slate-50 border border-slate-200 rounded px-2 py-1 max-w-xs truncate">
            {item.recommended.reason}
          </div>
        )}
      </div>

      <div className="grid grid-cols-2 gap-3">
        <StoreColumn
          store="kroger"
          products={item.kroger}
          quantity={item.quantity}
          isBest={bestStore === 'kroger'}
        />
        <StoreColumn
          store="walmart"
          products={item.walmart}
          quantity={item.quantity}
          isBest={bestStore === 'walmart'}
        />
      </div>
    </div>
  )
}
