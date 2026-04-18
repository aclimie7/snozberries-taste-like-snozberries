import { Header } from './components/layout/Header'
import { ShoppingListPanel } from './components/shopping-list/ShoppingListPanel'
import { CreditCardPanel } from './components/credit-cards/CreditCardPanel'
import { StoreRewardsPanel } from './components/store-rewards/StoreRewardsPanel'
import { ComparisonDashboard } from './components/comparison/ComparisonDashboard'

export default function App() {
  return (
    <div className="min-h-screen bg-slate-50">
      <Header />
      <div className="max-w-7xl mx-auto px-4 py-6">
        <div className="flex gap-6">
          <aside className="w-72 flex-shrink-0 space-y-4">
            <ShoppingListPanel />
            <StoreRewardsPanel />
            <CreditCardPanel />
          </aside>
          <main className="flex-1 min-w-0">
            <ComparisonDashboard />
          </main>
        </div>
      </div>
    </div>
  )
}
