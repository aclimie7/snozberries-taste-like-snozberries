export type RewardType = 'cashback' | 'points'

export type CreditCard = {
  id: string
  name: string
  reward_type: RewardType
  earn_rates: Record<string, number>
  cents_per_point: number
  is_active: boolean
}
