import type { StoreRewardsProgram } from '../types/store-rewards'

const DEFAULT_PROGRAMS: StoreRewardsProgram[] = [
  {
    store: 'kroger',
    program_name: 'Kroger Plus',
    enrolled: false,
    store_cashback_rate: 0,
    fuel_points_per_dollar: 1,
  },
  {
    store: 'walmart',
    program_name: 'Walmart+',
    enrolled: false,
    store_cashback_rate: 0.01,
    fuel_points_per_dollar: 0,
  },
]

export type StoreRewardsState = {
  programs: StoreRewardsProgram[]
  toggleEnrollment: (store: 'kroger' | 'walmart') => void
}

export const storeRewardsSlice = (set: (fn: (s: StoreRewardsState) => Partial<StoreRewardsState>) => void): StoreRewardsState => ({
  programs: DEFAULT_PROGRAMS,
  toggleEnrollment: (store) =>
    set((s) => ({
      programs: s.programs.map((p) =>
        p.store === store ? { ...p, enrolled: !p.enrolled } : p,
      ),
    })),
})
