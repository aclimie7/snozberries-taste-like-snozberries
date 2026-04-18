import type { ComparisonResult } from '../types/product'

export type ComparisonState = {
  result: ComparisonResult | null
  loading: boolean
  error: string | null
  setResult: (r: ComparisonResult) => void
  setLoading: (v: boolean) => void
  setError: (e: string | null) => void
  clearResult: () => void
}

export const comparisonSlice = (set: (fn: (s: ComparisonState) => Partial<ComparisonState>) => void): ComparisonState => ({
  result: null,
  loading: false,
  error: null,
  setResult: (r) => set(() => ({ result: r, error: null, loading: false })),
  setLoading: (v) => set(() => ({ loading: v })),
  setError: (e) => set(() => ({ error: e, loading: false })),
  clearResult: () => set(() => ({ result: null, error: null })),
})
