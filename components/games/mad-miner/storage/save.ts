export type Upgrades = {
  fuelEff: number
  hookPower: number
  digSpeed: number
}

export type SaveData = {
  version: string
  highScore: number
  upgrades: Upgrades
}

const KEY = 'mad-miner-save-v0.1'

export const defaultUpgrades: Upgrades = { fuelEff: 0, hookPower: 0, digSpeed: 0 }

export function loadSave(): SaveData {
  if (typeof window === 'undefined') return { version: '0.1', highScore: 0, upgrades: { ...defaultUpgrades } }
  try {
    const raw = localStorage.getItem(KEY)
    if (!raw) return { version: '0.1', highScore: 0, upgrades: { ...defaultUpgrades } }
    const data = JSON.parse(raw) as SaveData
    if (!data.version) data.version = '0.1'
    if (!data.upgrades) data.upgrades = { ...defaultUpgrades }
    if (typeof data.highScore !== 'number') data.highScore = 0
    return data
  } catch {
    return { version: '0.1', highScore: 0, upgrades: { ...defaultUpgrades } }
  }
}

export function saveSave(data: SaveData): void {
  if (typeof window === 'undefined') return
  try {
    localStorage.setItem(KEY, JSON.stringify(data))
  } catch {
    // ignore
  }
}
