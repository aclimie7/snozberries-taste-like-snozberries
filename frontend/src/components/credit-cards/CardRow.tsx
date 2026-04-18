import { useStore } from '../../store'
import type { CreditCard } from '../../types/credit-card'

function rateDisplay(card: CreditCard, cat: string) {
  const rate = card.earn_rates[cat] ?? card.earn_rates['default'] ?? 0
  if (rate === 0) return null
  if (card.reward_type === 'cashback') return `${(rate * 100).toFixed(1)}%`
  return `${rate}x`
}

export function CardRow({ card }: { card: CreditCard }) {
  const removeCard = useStore((s) => s.removeCard)
  const toggleCard = useStore((s) => s.toggleCard)

  return (
    <div className={`rounded-lg border p-3 space-y-1.5 transition-colors ${card.is_active ? 'border-blue-200 bg-blue-50' : 'border-slate-200 bg-white opacity-60'}`}>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={card.is_active}
            onChange={() => toggleCard(card.id)}
            className="accent-blue-600"
          />
          <span className="text-sm font-medium text-slate-700">{card.name}</span>
          <span className="text-xs bg-slate-200 text-slate-600 rounded px-1">
            {card.reward_type === 'cashback' ? 'Cash' : `Pts @${card.cents_per_point}¢`}
          </span>
        </div>
        <button onClick={() => removeCard(card.id)} className="text-slate-300 hover:text-red-400 text-lg leading-none">×</button>
      </div>
      <div className="flex gap-3 text-xs text-slate-500">
        {rateDisplay(card, 'grocery') && <span>Grocery: <strong className="text-slate-700">{rateDisplay(card, 'grocery')}</strong></span>}
        {rateDisplay(card, 'general_merchandise') && <span>GM: <strong className="text-slate-700">{rateDisplay(card, 'general_merchandise')}</strong></span>}
        {rateDisplay(card, 'default') && <span>Other: <strong className="text-slate-700">{rateDisplay(card, 'default')}</strong></span>}
      </div>
    </div>
  )
}
