import type { Store } from './product'

export type StoreRewardsProgram = {
  store: Store
  program_name: string
  enrolled: boolean
  store_cashback_rate: number
  fuel_points_per_dollar: number
}
