import React from 'react'

type HUDProps = {
  gold: number
  fuel: number
  o2: number
  heat: number
  depth: number
  eventLabel?: string | null
  highScore: number
}

const Bar: React.FC<{ label: string, value: number, color: string }> = ({ label, value, color }) => (
  <div className="flex items-center gap-2 text-xs">
    <div className="w-12 text-right opacity-80">{label}</div>
    <div className="w-28 h-2 bg-black/20 rounded">
      <div className="h-2 rounded" style={{ width: `${Math.max(0, Math.min(100, value))}%`, backgroundColor: color }} />
    </div>
  </div>
)

export const HUD: React.FC<HUDProps> = ({ gold, fuel, o2, heat, depth, eventLabel, highScore }) => {
  return (
    <div className="fixed top-2 left-1/2 -translate-x-1/2 bg-white/60 dark:bg-black/40 backdrop-blur px-3 py-2 rounded shadow z-20">
      <div className="flex items-center gap-4">
        <div className="text-sm">Gold: {gold}</div>
        <Bar label="Fuel" value={fuel} color="#10b981" />
        <Bar label="O2" value={o2} color="#60a5fa" />
        <Bar label="Heat" value={heat} color="#f43f5e" />
        <div className="text-xs opacity-80">Depth: {Math.floor(depth)}</div>
        <div className="text-xs opacity-80">Best: {highScore}</div>
        {eventLabel && (
          <div className="text-xs px-2 py-1 rounded bg-yellow-500/80 text-white">{eventLabel}</div>
        )}
      </div>
    </div>
  )
}
