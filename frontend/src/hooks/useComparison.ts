import { useStore } from '../store'
import { fetchComparison } from '../api/shopping'

export function useComparison() {
  const items = useStore((s) => s.items)
  const zipCode = useStore((s) => s.zipCode)
  const cards = useStore((s) => s.cards)
  const programs = useStore((s) => s.programs)
  const setResult = useStore((s) => s.setResult)
  const setLoading = useStore((s) => s.setLoading)
  const setError = useStore((s) => s.setError)
  const loading = useStore((s) => s.loading)

  const canCompare = items.length > 0 && zipCode.length === 5

  const runComparison = async () => {
    if (!canCompare) return
    setLoading(true)
    setError(null)
    try {
      const result = await fetchComparison(items, zipCode, cards, programs)
      setResult(result)
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Failed to fetch prices. Please try again.'
      setError(message)
    }
  }

  return { runComparison, loading, canCompare }
}
