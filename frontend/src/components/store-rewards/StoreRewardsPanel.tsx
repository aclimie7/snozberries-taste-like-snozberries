import { useStore } from '../../store'

const PROGRAM_INFO: Record<string, { icon: string; description: string }> = {
  kroger: {
    icon: '🔵',
    description: 'Unlocks member/sale prices · Earns fuel points (1 pt/$1)',
  },
  walmart: {
    icon: '🟡',
    description: 'Earns 1% Walmart Cash on eligible purchases',
  },
}

export function StoreRewardsPanel() {
  const programs = useStore((s) => s.programs)
  const toggleEnrollment = useStore((s) => s.toggleEnrollment)

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-4 space-y-3">
      <h2 className="font-semibold text-slate-800 text-base">Store Rewards</h2>
      <p className="text-xs text-slate-500">Toggle programs you're enrolled in.</p>

      <div className="space-y-2">
        {programs.map((prog) => {
          const info = PROGRAM_INFO[prog.store]
          return (
            <label
              key={prog.store}
              className={`flex items-start gap-3 p-3 rounded-lg border cursor-pointer transition-colors ${
                prog.enrolled ? 'border-green-200 bg-green-50' : 'border-slate-200 bg-white'
              }`}
            >
              <input
                type="checkbox"
                checked={prog.enrolled}
                onChange={() => toggleEnrollment(prog.store as 'kroger' | 'walmart')}
                className="mt-0.5 accent-green-600"
              />
              <div>
                <div className="text-sm font-medium text-slate-700">
                  {info?.icon} {prog.program_name}
                </div>
                <div className="text-xs text-slate-500 mt-0.5">{info?.description}</div>
              </div>
            </label>
          )
        })}
      </div>
    </div>
  )
}
