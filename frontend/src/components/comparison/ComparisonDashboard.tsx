import { useStore } from '../../store'
import { ItemComparisonCard } from './ItemComparisonCard'
import { SavingsSummary } from './SavingsSummary'
import { DemoModeBanner } from '../shared/DemoModeBanner'
import { ErrorBanner } from '../shared/ErrorBanner'
import { LoadingSpinner } from '../shared/LoadingSpinner'
import { EmptyState } from '../shared/EmptyState'

export function ComparisonDashboard() {
  const result = useStore((s) => s.result)
  const loading = useStore((s) => s.loading)
  const error = useStore((s) => s.error)

  if (loading) return <LoadingSpinner />
  if (error) return <ErrorBanner message={error} />
  if (!result) return <EmptyState />

  return (
    <div className="space-y-4">
      {result.demo_mode && <DemoModeBanner />}
      {result.warnings.length > 0 && (
        <div className="bg-orange-50 border border-orange-200 text-orange-800 text-sm px-4 py-2 rounded-lg">
          {result.warnings.map((w, i) => <p key={i}>{w}</p>)}
        </div>
      )}

      <SavingsSummary result={result} />

      <div className="space-y-3">
        {result.items.map((item) => (
          <ItemComparisonCard key={item.query} item={item} />
        ))}
      </div>
    </div>
  )
}
