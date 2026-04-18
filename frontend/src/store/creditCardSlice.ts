import { nanoid } from 'nanoid'
import type { CreditCard } from '../types/credit-card'

export type CreditCardState = {
  cards: CreditCard[]
  addCard: (card: Omit<CreditCard, 'id'>) => void
  removeCard: (id: string) => void
  toggleCard: (id: string) => void
  updateCard: (id: string, updates: Partial<Omit<CreditCard, 'id'>>) => void
}

export const creditCardSlice = (set: (fn: (s: CreditCardState) => Partial<CreditCardState>) => void): CreditCardState => ({
  cards: [],
  addCard: (card) => set((s) => ({ cards: [...s.cards, { ...card, id: nanoid() }] })),
  removeCard: (id) => set((s) => ({ cards: s.cards.filter((c) => c.id !== id) })),
  toggleCard: (id) =>
    set((s) => ({ cards: s.cards.map((c) => (c.id === id ? { ...c, is_active: !c.is_active } : c)) })),
  updateCard: (id, updates) =>
    set((s) => ({ cards: s.cards.map((c) => (c.id === id ? { ...c, ...updates } : c)) })),
})
