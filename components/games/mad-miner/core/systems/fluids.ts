import { GameState } from '../state'

export function updateLava(state: GameState, dt: number): void {
  // Lava rises faster as time passes
  const t = (state.time - state.runStartTime) / state.runDuration
  const base = 0.02 // tiles per second
  const amount = (base + t * 0.05) * dt
  state.map.lavaLevel -= amount
  if (state.map.lavaLevel < 0) state.map.lavaLevel = 0
}

export function nearLavaHeat(state: GameState): number {
  // Heat increases when close to lava level
  const tileY = Math.floor(state.player.pos.y / state.config.tile)
  const dist = Math.max(0, tileY - state.map.lavaLevel)
  const heat = dist < 8 ? (8 - dist) * 0.6 : 0
  return heat
}
