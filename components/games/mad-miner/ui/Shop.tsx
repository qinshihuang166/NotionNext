import React from 'react'
import type { Upgrades } from '../storage/save'

type ShopProps = {
  open: boolean
  onClose: () => void
  gold: number
  setGold: (g: number) => void
  upgrades: Upgrades
  setUpgrades: (u: Upgrades) => void
}

const itemDefs: Array<{ key: keyof Upgrades, title: string, desc: string, baseCost: number }>
  = [
    { key: 'fuelEff', title: '燃料效率', desc: '减少燃料消耗', baseCost: 30 },
    { key: 'hookPower', title: '抓钩力量', desc: '更快回收，提高重量上限', baseCost: 40 },
    { key: 'digSpeed', title: '挖掘速度', desc: '更快移动与挖掘', baseCost: 50 }
  ]

export const Shop: React.FC<ShopProps> = ({ open, onClose, gold, setGold, upgrades, setUpgrades }) => {
  if (!open) return null
  return (
    <div className="fixed inset-0 z-30 bg-black/40 flex items-center justify-center">
      <div className="bg-white dark:bg-neutral-900 rounded-lg p-4 w-80 shadow-lg">
        <div className="flex items-center justify-between mb-3">
          <div className="font-bold">矿工商店</div>
          <button className="text-sm opacity-70" onClick={onClose}>关闭</button>
        </div>
        <div className="text-sm mb-2">当前金币：{gold}</div>
        <div className="space-y-2">
          {itemDefs.map(def => {
            const lvl = upgrades[def.key]
            const cost = Math.floor(def.baseCost * Math.pow(1.6, lvl))
            const affordable = gold >= cost
            return (
              <div key={String(def.key)} className="p-2 rounded border border-neutral-200 dark:border-neutral-800 flex items-center justify-between">
                <div>
                  <div className="text-sm">{def.title} Lv.{lvl}</div>
                  <div className="text-xs opacity-70">{def.desc}</div>
                </div>
                <button
                  disabled={!affordable}
                  onClick={() => {
                    if (!affordable) return
                    setGold(gold - cost)
                    setUpgrades({ ...upgrades, [def.key]: lvl + 1 })
                  }}
                  className={`px-2 py-1 rounded text-white text-xs ${affordable ? 'bg-indigo-600' : 'bg-neutral-400 dark:bg-neutral-700'}`}
                >
                  购买({cost})
                </button>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}
