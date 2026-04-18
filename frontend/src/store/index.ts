import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { shoppingListSlice, type ShoppingListState } from './shoppingListSlice'
import { creditCardSlice, type CreditCardState } from './creditCardSlice'
import { storeRewardsSlice, type StoreRewardsState } from './storeRewardsSlice'
import { comparisonSlice, type ComparisonState } from './comparisonSlice'

type AppState = ShoppingListState & CreditCardState & StoreRewardsState & ComparisonState

export const useStore = create<AppState>()(
  persist(
    (set) => ({
      ...shoppingListSlice(set as Parameters<typeof shoppingListSlice>[0]),
      ...creditCardSlice(set as Parameters<typeof creditCardSlice>[0]),
      ...storeRewardsSlice(set as Parameters<typeof storeRewardsSlice>[0]),
      ...comparisonSlice(set as Parameters<typeof comparisonSlice>[0]),
    }),
    {
      name: 'shopping-app-storage',
      partialState: (state: AppState) => ({
        items: state.items,
        zipCode: state.zipCode,
        cards: state.cards,
        programs: state.programs,
      }),
    } as Parameters<typeof persist>[1],
  ),
)
