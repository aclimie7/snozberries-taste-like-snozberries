export type Store = 'kroger' | 'walmart'

export type ProductCategory = 'grocery' | 'general_merchandise'

export type PriceBreakdown = {
  base_price: number
  sale_price: number | null
  coupon_savings: number
  store_rewards_savings: number
  effective_price: number
  cc_reward_value: number
  final_price: number
  cc_reward_detail: string
  store_reward_detail: string
}

export type NormalizedProduct = {
  store: Store
  product_id: string
  name: string
  brand: string
  upc: string | null
  size: string
  image_url: string | null
  category: ProductCategory
  price: PriceBreakdown
  on_sale: boolean
  has_digital_coupon: boolean
  in_stock: boolean
  score: number
}

export type Recommendation = {
  store: Store
  product: NormalizedProduct
  reason: string
}

export type ItemComparison = {
  query: string
  quantity: number
  kroger: NormalizedProduct[]
  walmart: NormalizedProduct[]
  recommended: Recommendation | null
}

export type SplitRecommendation = {
  kroger_items: string[]
  walmart_items: string[]
  split_savings: number
}

export type ComparisonSummary = {
  kroger_total: number
  walmart_total: number
  best_store: Store
  total_savings: number
  rewards_applied: number
  split_recommendation: SplitRecommendation | null
}

export type ComparisonResult = {
  items: ItemComparison[]
  summary: ComparisonSummary
  demo_mode: boolean
  warnings: string[]
}
