import type { NormalizedProduct, Store } from '../../types/product'
import { PriceBadge } from './PriceBadge'
import { RewardsBreakdownTooltip } from './RewardsBreakdownTooltip'

const STORE_LABELS: Record<Store, { name: string; color: string; bg: string }> = {
  kroger: { name: 'Kroger', color: 'text-blue-700', bg: 'bg-blue-50 border-blue-100' },
  walmart: { name: 'Walmart', color: 'text-yellow-700', bg: 'bg-yellow-50 border-yellow-100' },
}

export function StoreColumn({ store, products, quantity, isBest }: {
  store: Store
  products: NormalizedProduct[]
  quantity: number
  isBest: boolean
}) {
  const label = STORE_LABELS[store]
  const top = products[0]

  return (
    <div className={`rounded-lg border p-3 space-y-2 ${isBest ? label.bg + ' ring-2 ring-offset-1 ' + (store === 'kroger' ? 'ring-blue-300' : 'ring-yellow-300') : 'border-slate-100 bg-slate-50'}`}>
      <div className="flex items-center justify-between">
        <span className={`font-semibold text-sm ${label.color}`}>{label.name}</span>
        {isBest && <span className="text-xs bg-green-100 text-green-700 px-1.5 py-0.5 rounded font-medium">Best deal</span>}
      </div>

      {products.length === 0 ? (
        <p className="text-xs text-slate-400 italic">No results</p>
      ) : (
        <>
          {top && (
            <div className="space-y-1">
              <div className="flex gap-2">
                {top.image_url && (
                  <img src={top.image_url} alt={top.name} className="w-12 h-12 object-contain rounded bg-white border border-slate-100 flex-shrink-0" />
                )}
                <div className="flex-1 min-w-0">
                  <p className="text-xs font-medium text-slate-700 line-clamp-2 leading-tight">{top.name}</p>
                  {top.size && <p className="text-xs text-slate-400">{top.size}</p>}
                  {top.on_sale && (
                    <span className="text-xs bg-red-100 text-red-600 px-1 rounded">On Sale</span>
                  )}
                </div>
                <PriceBadge product={top} />
              </div>
              {quantity > 1 && (
                <p className="text-xs text-slate-500 text-right">
                  ×{quantity} = <strong>${(top.price.final_price * quantity).toFixed(2)}</strong>
                </p>
              )}
              <div className="text-right">
                <RewardsBreakdownTooltip product={top} />
              </div>
            </div>
          )}

          {products.length > 1 && (
            <details className="text-xs">
              <summary className="cursor-pointer text-slate-400 hover:text-slate-600">
                {products.length - 1} more option{products.length > 2 ? 's' : ''}
              </summary>
              <div className="mt-2 space-y-2 pt-2 border-t border-slate-100">
                {products.slice(1).map((p) => (
                  <div key={p.product_id} className="flex items-center justify-between gap-2">
                    <p className="text-slate-600 text-xs truncate flex-1">{p.name} {p.size && `· ${p.size}`}</p>
                    <span className="text-xs font-semibold text-slate-700 flex-shrink-0">${p.price.final_price.toFixed(2)}</span>
                  </div>
                ))}
              </div>
            </details>
          )}
        </>
      )}
    </div>
  )
}
