import { ActiveEvent, EventType, GameState } from '../state'

function createEvent(type: EventType, now: number): ActiveEvent {
  switch (type) {
    case 'quake':
      return { type, endsAt: now + 30_000, priceMul: 1, digSpeedMul: 0.9, heatRateMul: 1 }
    case 'crash':
      return { type, endsAt: now + 25_000, priceMul: 0.6, digSpeedMul: 1, heatRateMul: 1 }
    case 'overload':
      return { type, endsAt: now + 20_000, priceMul: 1.2, digSpeedMul: 1.2, heatRateMul: 1.5 }
  }
}

export function maybeStartRandomEvent(state: GameState, now: number): void {
  if (state.event) return
  // chance every 10s
  if ((now - state.runStartTime) % 10_000 < 50) {
    const r = state.rng.nextFloat()
    const type: EventType = r < 0.33 ? 'quake' : r < 0.66 ? 'crash' : 'overload'
    state.event = createEvent(type, now)
    state.mode = 'EVENT'
  }
}

export function updateEvent(state: GameState, now: number): void {
  if (!state.event) return
  if (now >= state.event.endsAt) {
    state.event = null
    state.mode = 'DIG'
  }
}
