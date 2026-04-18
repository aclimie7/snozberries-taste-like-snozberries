import client from './client'
import type { ComparisonResult } from '../types/product'
import type { ShoppingItem } from '../types/shopping-list'
import type { CreditCard } from '../types/credit-card'
import type { StoreRewardsProgram } from '../types/store-rewards'

export async function fetchComparison(
  items: ShoppingItem[],
  zipCode: string,
  creditCards: CreditCard[],
  storeRewardsPrograms: StoreRewardsProgram[],
  demoMode = false,
): Promise<ComparisonResult> {
  const payload = {
    items: items.map(({ name, quantity, unit }) => ({ name, quantity, unit })),
    zip_code: zipCode,
    credit_cards: creditCards,
    store_rewards_programs: storeRewardsPrograms,
    demo_mode: demoMode,
  }
  const res = await client.post<ComparisonResult>('/compare', payload)
  return res.data
}
