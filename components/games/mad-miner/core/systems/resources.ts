import { GameState } from '../state'

export type ResourceDelta = {
  fuel: number
  o2: number
  heat: number
}

export function updateResources(state: GameState, dt: number, digging: boolean): void {
  const upgrades = state.upgrades
  const fuelEffMul = 1 - Math.min(0.5, upgrades.fuelEff * 0.1)
  const evHeatMul = state.event?.heatRateMul ?? 1
  const evDigMul = state.event?.digSpeedMul ?? 1

  let fuelUse = digging ? 8 : 2
  let o2Use = 3
  let heatGain = digging ? 7 : 2

  fuelUse *= fuelEffMul
  heatGain *= evHeatMul
  fuelUse *= 1 / Math.max(0.5, evDigMul)

  state.res.fuel = Math.max(0, state.res.fuel - fuelUse * dt)
  state.res.o2 = Math.max(0, state.res.o2 - o2Use * dt)
  state.res.heat = Math.min(100, state.res.heat + heatGain * dt)
}

export function isDead(state: GameState): boolean {
  return state.res.fuel <= 0 || state.res.o2 <= 0 || state.res.heat >= 100
}
