import { nanoid } from 'nanoid'
import type { ShoppingItem } from '../types/shopping-list'

export type ShoppingListState = {
  items: ShoppingItem[]
  zipCode: string
  addItem: (name: string, quantity?: number) => void
  removeItem: (id: string) => void
  updateQuantity: (id: string, qty: number) => void
  updateName: (id: string, name: string) => void
  setZipCode: (zip: string) => void
  clearItems: () => void
}

export const shoppingListSlice = (set: (fn: (s: ShoppingListState) => Partial<ShoppingListState>) => void): ShoppingListState => ({
  items: [],
  zipCode: '',
  addItem: (name, quantity = 1) =>
    set((s) => ({ items: [...s.items, { id: nanoid(), name: name.trim(), quantity }] })),
  removeItem: (id) => set((s) => ({ items: s.items.filter((i) => i.id !== id) })),
  updateQuantity: (id, qty) =>
    set((s) => ({ items: s.items.map((i) => (i.id === id ? { ...i, quantity: Math.max(1, qty) } : i)) })),
  updateName: (id, name) =>
    set((s) => ({ items: s.items.map((i) => (i.id === id ? { ...i, name } : i)) })),
  setZipCode: (zip) => set(() => ({ zipCode: zip })),
  clearItems: () => set(() => ({ items: [] })),
})
