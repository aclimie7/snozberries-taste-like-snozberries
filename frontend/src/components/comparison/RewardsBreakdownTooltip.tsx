import { useState } from 'react'
import type { NormalizedProduct } from '../../types/product'

export function RewardsBreakdownTooltip({ product }: { product: NormalizedProduct }) {
  const [show, setShow] = useState(false)
  const { price } = product
  const hasDetails = price.cc_reward_detail || price.store_reward_detail

  if (!hasDetails) return null

  return (
    <div className="relative inline-block">
      <button
        className="text-xs text-slate-400 hover:text-blue-600 underline"
        onMouseEnter={() => setShow(true)}
        onMouseLeave={() => setShow(false)}
        onClick={() => setShow((s) => !s)}
      >
        details
      </button>
      {show && (
        <div className="absolute bottom-full right-0 mb-1 w-64 bg-white border border-slate-200 rounded-lg shadow-lg p-3 z-10 text-left space-y-1">
          {price.store_reward_detail && (
            <div className="text-xs text-green-700">
              <span className="font-medium">Store: </span>{price.store_reward_detail}
            </div>
          )}
          {price.cc_reward_detail && (
            <div className="text-xs text-blue-700">
              <span className="font-medium">Card: </span>{price.cc_reward_detail}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
