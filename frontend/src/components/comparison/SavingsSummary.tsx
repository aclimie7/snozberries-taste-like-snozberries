import type { ComparisonResult } from '../../types/product'

function fmt(n: number) { return `$${n.toFixed(2)}` }

const STORE_NAMES = { kroger: 'Kroger', walmart: 'Walmart' }

export function SavingsSummary({ result }: { result: ComparisonResult }) {
  const { summary } = result
  const bestName = STORE_NAMES[summary.best_store]
  const worstName = summary.best_store === 'kroger' ? 'Walmart' : 'Kroger'
  const worstTotal = summary.best_store === 'kroger' ? summary.walmart_total : summary.kroger_total

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 space-y-4">
      <h2 className="font-bold text-slate-800 text-lg">Summary</h2>

      <div className="grid grid-cols-2 gap-4">
        <div className={`rounded-lg p-3 text-center border ${summary.best_store === 'kroger' ? 'border-blue-300 bg-blue-50' : 'border-slate-100 bg-slate-50'}`}>
          <div className="text-xs text-slate-500 mb-1">Kroger Total</div>
          <div className={`text-2xl font-bold ${summary.best_store === 'kroger' ? 'text-blue-700' : 'text-slate-700'}`}>{fmt(summary.kroger_total)}</div>
          {summary.best_store === 'kroger' && <div className="text-xs text-green-600 mt-1">Best store</div>}
        </div>

        <div className={`rounded-lg p-3 text-center border ${summary.best_store === 'walmart' ? 'border-yellow-300 bg-yellow-50' : 'border-slate-100 bg-slate-50'}`}>
          <div className="text-xs text-slate-500 mb-1">Walmart Total</div>
          <div className={`text-2xl font-bold ${summary.best_store === 'walmart' ? 'text-yellow-700' : 'text-slate-700'}`}>{fmt(summary.walmart_total)}</div>
          {summary.best_store === 'walmart' && <div className="text-xs text-green-600 mt-1">Best store</div>}
        </div>
      </div>

      {summary.total_savings > 0 && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-3 text-center">
          <p className="text-sm text-green-800">
            Shop at <strong>{bestName}</strong> and save <strong>{fmt(summary.total_savings)}</strong> vs {worstName} ({fmt(worstTotal)})
          </p>
        </div>
      )}

      {summary.rewards_applied > 0 && (
        <div className="text-sm text-slate-600 flex items-center gap-2">
          <span className="text-blue-500">💳</span>
          <span>Rewards applied: <strong>{fmt(summary.rewards_applied)}</strong> across all items</span>
        </div>
      )}

      {summary.split_recommendation && (
        <div className="border border-purple-200 bg-purple-50 rounded-lg p-4 space-y-2">
          <div className="flex items-center gap-2">
            <span>✂️</span>
            <span className="font-semibold text-purple-800 text-sm">
              Split your trip — save an extra {fmt(summary.split_recommendation.split_savings)}
            </span>
          </div>
          <div className="grid grid-cols-2 gap-2 text-xs">
            <div>
              <div className="font-medium text-blue-700 mb-1">Buy at Kroger:</div>
              <ul className="space-y-0.5 text-slate-600">
                {summary.split_recommendation.kroger_items.map((item) => (
                  <li key={item} className="capitalize">• {item}</li>
                ))}
              </ul>
            </div>
            <div>
              <div className="font-medium text-yellow-700 mb-1">Buy at Walmart:</div>
              <ul className="space-y-0.5 text-slate-600">
                {summary.split_recommendation.walmart_items.map((item) => (
                  <li key={item} className="capitalize">• {item}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
