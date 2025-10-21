import { GameState, Vec2, HookState, Ore } from '../state'
import { clamp } from '../../utils/easing'

export function updateHookPhysics(state: GameState, dt: number): void {
  const hook = state.hook
  const p = state.player
  if (state.mode !== 'HOOK') return
  // Rotate when idle
  if (!hook.fired && hook.rotating) {
    hook.angle += hook.speed * dt
    const limit = Math.PI / 2.2
    if (hook.angle > limit) hook.speed = -Math.abs(hook.speed)
    if (hook.angle < -limit) hook.speed = Math.abs(hook.speed)
    hook.head.x = p.pos.x + Math.cos(hook.angle) * 10
    hook.head.y = p.pos.y + Math.sin(hook.angle) * 10
  }
  // When fired, extend then retract
  if (hook.fired) {
    hook.ropeLen += 200 * dt
    hook.head.x = p.pos.x + Math.cos(hook.angle) * hook.ropeLen
    hook.head.y = p.pos.y + Math.sin(hook.angle) * hook.ropeLen
    // bounds
    if (hook.head.x < 0 || hook.head.x > state.config.width || hook.head.y < 0 || hook.head.y > state.config.height) {
      hook.returning = true
    }
    // Check ore collision
    if (!hook.target) {
      const hit = hitOre(hook.head, state.ores)
      if (hit) {
        hook.target = hit
        hook.returning = true
      }
    }
    if (hook.returning) {
      const dx = p.pos.x - hook.head.x
      const dy = p.pos.y - hook.head.y
      const dist = Math.hypot(dx, dy)
      const retSpeed = 250 * (1 + state.upgrades.hookPower * 0.15)
      const step = Math.min(retSpeed * dt, dist)
      hook.head.x += (dx / (dist || 1)) * step
      hook.head.y += (dy / (dist || 1)) * step
      hook.ropeLen = Math.max(0, hook.ropeLen - step)
      if (hook.target) {
        hook.target.pos.x = hook.head.x
        hook.target.pos.y = hook.head.y
      }
      if (dist < 8) {
        // collect
        if (hook.target) {
          state.res.gold += Math.floor(hook.target.value * (state.event?.priceMul ?? 1))
          // remove ore
          state.ores = state.ores.filter(o => o.id !== hook.target!.id)
        }
        hook.fired = false
        hook.returning = false
        hook.target = null
        hook.ropeLen = 0
        state.mode = 'DIG'
      }
    }
  }
}

function hitOre(pt: Vec2, ores: Ore[]): Ore | null {
  for (const o of ores) {
    const d = Math.hypot(o.pos.x - pt.x, o.pos.y - pt.y)
    if (d < o.radius + 6) return o
  }
  return null
}

export function updatePlayerDigging(state: GameState, dt: number, inputDir: Vec2): void {
  if (state.mode !== 'DIG') return
  // Move player with dig speed mod
  const base = 60
  const digMul = 1 + state.upgrades.digSpeed * 0.2
  const evMul = state.event?.digSpeedMul ?? 1
  const speed = base * digMul * evMul
  const len = Math.hypot(inputDir.x, inputDir.y)
  const nx = len > 0 ? inputDir.x / len : 0
  const ny = len > 0 ? inputDir.y / len : 0
  state.player.pos.x = clamp(state.player.pos.x + nx * speed * dt, 8, state.config.width - 8)
  state.player.pos.y = clamp(state.player.pos.y + ny * speed * dt, 8, state.config.height - 8)
  // Depth
  state.player.depth = Math.max(state.player.depth, state.player.pos.y)
}
