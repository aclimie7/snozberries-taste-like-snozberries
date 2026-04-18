import { useStore } from '../../store'
import { AddCardForm } from './AddCardForm'
import { CardRow } from './CardRow'

export function CreditCardPanel() {
  const cards = useStore((s) => s.cards)

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-4 space-y-3">
      <h2 className="font-semibold text-slate-800 text-base">Credit Cards</h2>
      <p className="text-xs text-slate-500">Add your cards to optimize rewards at each store.</p>

      <div className="space-y-2">
        {cards.map((card) => (
          <CardRow key={card.id} card={card} />
        ))}
      </div>

      <AddCardForm />
    </div>
  )
}
