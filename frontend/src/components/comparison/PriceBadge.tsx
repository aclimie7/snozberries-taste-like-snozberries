import type { NormalizedProduct } from '../../types/product'

function fmt(n: number) {
  return `$${n.toFixed(2)}`
}

export function PriceBadge({ product }: { product: NormalizedProduct }) {
  const { price, on_sale } = product

  return (
    <div className="text-right space-y-0.5">
      <div className="flex items-baseline justify-end gap-1.5">
        <span className="text-lg font-bold text-slate-800">{fmt(price.final_price)}</span>
        {price.cc_reward_value > 0 && (
          <span className="text-xs text-green-600 font-medium">final</span>
        )}
      </div>

      {(on_sale || price.sale_price) && (
        <div className="flex items-center justify-end gap-1">
          <span className="line-through text-xs text-slate-400">{fmt(price.base_price)}</span>
          <span className="text-xs bg-red-100 text-red-700 px-1 rounded font-medium">SALE</span>
        </div>
      )}

      {price.store_rewards_savings > 0 && (
        <div className="text-xs text-green-600">−{fmt(price.store_rewards_savings)} store</div>
      )}

      {price.cc_reward_value > 0 && (
        <div className="text-xs text-blue-600">−{fmt(price.cc_reward_value)} rewards</div>
      )}

      {price.effective_price !== price.base_price && !on_sale && price.store_rewards_savings === 0 && (
        <div className="text-xs text-slate-400">{fmt(price.effective_price)}</div>
      )}
    </div>
  )
}
