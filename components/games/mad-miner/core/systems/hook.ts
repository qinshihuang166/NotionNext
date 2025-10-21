import { GameState } from '../state'

export function fireHook(state: GameState): void {
  if (state.mode !== 'HOOK') return
  if (state.hook.fired) return
  state.hook.fired = true
  state.hook.returning = false
  state.hook.ropeLen = 10
}

export function setMagnetize(state: GameState, on: boolean): void {
  state.hook.magnetizing = on
}
