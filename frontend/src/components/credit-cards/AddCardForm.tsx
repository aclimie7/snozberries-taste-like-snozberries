import { useState } from 'react'
import { useStore } from '../../store'
import type { RewardType } from '../../types/credit-card'

const CATEGORIES = [
  { key: 'grocery', label: 'Grocery' },
  { key: 'general_merchandise', label: 'General Merch' },
  { key: 'default', label: 'All Other' },
]

const POPULAR_CARDS = [
  { name: 'Amex Gold', reward_type: 'cashback' as RewardType, earn_rates: { grocery: 0.04, general_merchandise: 0.01, default: 0.01 }, cents_per_point: 1.0 },
  { name: 'Chase Sapphire Preferred', reward_type: 'points' as RewardType, earn_rates: { grocery: 3, general_merchandise: 1, default: 1 }, cents_per_point: 1.25 },
  { name: 'Capital One Savor', reward_type: 'cashback' as RewardType, earn_rates: { grocery: 0.03, general_merchandise: 0.01, default: 0.01 }, cents_per_point: 1.0 },
  { name: 'Citi Double Cash', reward_type: 'cashback' as RewardType, earn_rates: { grocery: 0.02, general_merchandise: 0.02, default: 0.02 }, cents_per_point: 1.0 },
]

export function AddCardForm() {
  const addCard = useStore((s) => s.addCard)
  const [open, setOpen] = useState(false)
  const [name, setName] = useState('')
  const [rewardType, setRewardType] = useState<RewardType>('cashback')
  const [earnRates, setEarnRates] = useState<Record<string, string>>({ grocery: '', general_merchandise: '', default: '' })
  const [cpp, setCpp] = useState('1.0')

  const handleQuickAdd = (preset: typeof POPULAR_CARDS[0]) => {
    addCard({ ...preset, is_active: true })
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!name.trim()) return
    const rates: Record<string, number> = {}
    for (const { key } of CATEGORIES) {
      const v = parseFloat(earnRates[key] || '0')
      if (!isNaN(v) && v > 0) rates[key] = rewardType === 'cashback' ? v / 100 : v
    }
    addCard({
      name: name.trim(),
      reward_type: rewardType,
      earn_rates: rates,
      cents_per_point: parseFloat(cpp) || 1.0,
      is_active: true,
    })
    setName('')
    setEarnRates({ grocery: '', general_merchandise: '', default: '' })
    setOpen(false)
  }

  return (
    <div className="space-y-2">
      <div className="text-xs font-medium text-slate-500 mb-1">Quick add popular cards:</div>
      <div className="flex flex-wrap gap-1">
        {POPULAR_CARDS.map((card) => (
          <button
            key={card.name}
            onClick={() => handleQuickAdd(card)}
            className="text-xs bg-slate-100 hover:bg-blue-50 hover:text-blue-700 border border-slate-200 hover:border-blue-300 rounded px-2 py-1 transition-colors"
          >
            + {card.name}
          </button>
        ))}
      </div>

      {!open ? (
        <button
          onClick={() => setOpen(true)}
          className="text-xs text-blue-600 hover:underline"
        >
          + Add custom card
        </button>
      ) : (
        <form onSubmit={handleSubmit} className="border border-slate-200 rounded-lg p-3 space-y-3 bg-slate-50">
          <input
            className="w-full border border-slate-300 rounded px-2 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-blue-400"
            placeholder="Card name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
          <div className="flex gap-2">
            <label className="flex items-center gap-1 text-xs cursor-pointer">
              <input type="radio" value="cashback" checked={rewardType === 'cashback'} onChange={() => setRewardType('cashback')} />
              Cashback %
            </label>
            <label className="flex items-center gap-1 text-xs cursor-pointer">
              <input type="radio" value="points" checked={rewardType === 'points'} onChange={() => setRewardType('points')} />
              Points (x per $1)
            </label>
          </div>
          {rewardType === 'points' && (
            <div>
              <label className="text-xs text-slate-500">Cents per point (CPP)</label>
              <input
                type="number"
                step="0.1"
                min="0.1"
                max="5"
                className="w-full border border-slate-300 rounded px-2 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-blue-400"
                value={cpp}
                onChange={(e) => setCpp(e.target.value)}
              />
            </div>
          )}
          {CATEGORIES.map(({ key, label }) => (
            <div key={key}>
              <label className="text-xs text-slate-500">
                {label} ({rewardType === 'cashback' ? '%' : 'x pts/$1'})
              </label>
              <input
                type="number"
                step={rewardType === 'cashback' ? '0.1' : '0.5'}
                min="0"
                max={rewardType === 'cashback' ? '20' : '20'}
                className="w-full border border-slate-300 rounded px-2 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-blue-400"
                placeholder={rewardType === 'cashback' ? 'e.g. 4' : 'e.g. 3'}
                value={earnRates[key]}
                onChange={(e) => setEarnRates((r) => ({ ...r, [key]: e.target.value }))}
              />
            </div>
          ))}
          <div className="flex gap-2">
            <button type="submit" className="flex-1 bg-blue-600 text-white text-sm rounded px-3 py-1.5 hover:bg-blue-700">
              Add Card
            </button>
            <button type="button" onClick={() => setOpen(false)} className="text-slate-500 text-sm hover:text-slate-700 px-2">
              Cancel
            </button>
          </div>
        </form>
      )}
    </div>
  )
}
