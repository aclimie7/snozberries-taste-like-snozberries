import { useState } from 'react'
import { useStore } from '../../store'

export function AddItemForm() {
  const addItem = useStore((s) => s.addItem)
  const [name, setName] = useState('')
  const [qty, setQty] = useState(1)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!name.trim()) return
    addItem(name.trim(), qty)
    setName('')
    setQty(1)
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <input
        className="flex-1 border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        placeholder="Add item (e.g. milk)"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <input
        type="number"
        min={1}
        max={99}
        className="w-16 border border-slate-300 rounded-lg px-2 py-2 text-sm text-center focus:outline-none focus:ring-2 focus:ring-blue-500"
        value={qty}
        onChange={(e) => setQty(Number(e.target.value))}
      />
      <button
        type="submit"
        className="bg-blue-600 text-white rounded-lg px-4 py-2 text-sm font-medium hover:bg-blue-700 disabled:opacity-50"
        disabled={!name.trim()}
      >
        Add
      </button>
    </form>
  )
}
