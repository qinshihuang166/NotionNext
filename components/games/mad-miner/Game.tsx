import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { createInitialState, GameConfig, GameState, Vec2 } from './core/state'
import { updateHookPhysics, updatePlayerDigging } from './core/systems/physics'
import { updateLava, nearLavaHeat } from './core/systems/fluids'
import { updateResources, isDead } from './core/systems/resources'
import { maybeStartRandomEvent, updateEvent } from './core/systems/events'
import { digAt, generateCave, applyQuake } from './core/map'
import { fireHook } from './core/systems/hook'
import { HUD } from './ui/HUD'
import { Buttons } from './ui/Buttons'
import { Shop } from './ui/Shop'
import { loadSave, saveSave, defaultUpgrades, Upgrades } from './storage/save'
import { clamp } from './utils/easing'

// Audio utility: unlocked on first touch
function useAudio(): { play: (freq: number, time?: number) => void; unlocked: boolean; unlock: () => void } {
  const ctxRef = useRef<AudioContext | null>(null)
  const [unlocked, setUnlocked] = useState(false)
  const unlock = useCallback(() => {
    if (typeof window === 'undefined') return
    if (!ctxRef.current) ctxRef.current = new (window.AudioContext || (window as any).webkitAudioContext)()
    if (ctxRef.current.state === 'suspended') {
      ctxRef.current.resume().then(() => setUnlocked(true)).catch(() => setUnlocked(false))
    } else {
      setUnlocked(true)
    }
  }, [])
  const play = useCallback((freq: number, time: number = 0.05) => {
    const ctx = ctxRef.current
    if (!ctx || ctx.state !== 'running') return
    const osc = ctx.createOscillator()
    const gain = ctx.createGain()
    osc.frequency.value = freq
    gain.gain.value = 0.06
    osc.connect(gain)
    gain.connect(ctx.destination)
    osc.start()
    osc.stop(ctx.currentTime + time)
  }, [])
  return { play, unlocked, unlock }
}

const useDevicePixelRatio = (): number => {
  const [dpr, setDpr] = useState(1)
  useEffect(() => {
    const handle = () => setDpr(Math.min(2, window.devicePixelRatio || 1))
    handle()
    window.addEventListener('resize', handle)
    return () => window.removeEventListener('resize', handle)
  }, [])
  return dpr
}

const MobileCanvas = React.forwardRef<HTMLCanvasElement, React.CanvasHTMLAttributes<HTMLCanvasElement>>((props, ref) => {
  return <canvas ref={ref} {...props} className={(props.className ?? '') + ' touch-none select-none bg-[#0b1020] rounded-lg shadow-lg'} />
})

const strokeText = (ctx: CanvasRenderingContext2D, text: string, x: number, y: number, color = 'white'): void => {
  ctx.fillStyle = 'black'
  ctx.strokeStyle = 'black'
  ctx.lineWidth = 4
  ctx.strokeText(text, x, y)
  ctx.fillStyle = color
  ctx.fillText(text, x, y)
}

const useSave = () => {
  const initial = useMemo(() => loadSave(), [])
  const [highScore, setHighScore] = useState(initial.highScore)
  const [upgrades, setUpgrades] = useState<Upgrades>(initial.upgrades || { ...defaultUpgrades })
  useEffect(() => {
    saveSave({ version: '0.1', highScore, upgrades })
  }, [highScore, upgrades])
  return { highScore, setHighScore, upgrades, setUpgrades }
}

const useVibrate = () => (pattern: number | number[]) => {
  if (typeof navigator !== 'undefined' && 'vibrate' in navigator) {
    try { navigator.vibrate(pattern as any) } catch {}
  }
}

const makeConfig = (width: number, height: number): GameConfig => ({ width, height, tile: 12 })

export const MadMinerGame: React.FC = () => {
  const containerRef = useRef<HTMLDivElement | null>(null)
  const canvasRef = useRef<HTMLCanvasElement | null>(null)
  const rafRef = useRef<number | null>(null)
  const [running, setRunning] = useState(false)
  const [paused, setPaused] = useState(false)
  const [shopOpen, setShopOpen] = useState(false)
  const [eventLabel, setEventLabel] = useState<string | null>(null)
  const dpr = useDevicePixelRatio()
  const { play, unlocked, unlock } = useAudio()
  const vibrate = useVibrate()
  const { highScore, setHighScore, upgrades, setUpgrades } = useSave()

  // game state ref
  const stateRef = useRef<GameState | null>(null)
  const [gold, setGold] = useState(0)

  const ensureState = useCallback(() => {
    if (!canvasRef.current) return
    const rect = canvasRef.current.getBoundingClientRect()
    const config = makeConfig(Math.max(320, Math.floor(rect.width)), Math.max(420, Math.floor(rect.height)))
    const s = createInitialState(config, upgrades, highScore)
    generateCave(s.map, s.rng)
    s.runStartTime = performance.now()
    s.nextPuzzleTime = s.runStartTime + 30_000
    stateRef.current = s
  }, [upgrades, highScore])

  // input state
  const joystickRef = useRef<{ active: boolean, id: number | null, origin: Vec2, dir: Vec2 }>({ active: false, id: null, origin: { x: 0, y: 0 }, dir: { x: 0, y: 0 } })
  const puzzleRef = useRef<{ drawing: boolean, points: Vec2[] }>({ drawing: false, points: [] })

  // main loop
  const loop = useCallback(() => {
    const s = stateRef.current
    const canvas = canvasRef.current
    if (!s || !canvas) return
    const ctx = canvas.getContext('2d')!

    const fixedDt = 1 / 60
    const now = performance.now()
    s.time = now
    if (!s.paused) {
      // stage transitions
      if (s.mode === 'HOOK' && !s.hook.fired) {
        // idle rotate
      }
      // update systems
      updateHookPhysics(s, fixedDt)

      const moving = Math.hypot(joystickRef.current.dir.x, joystickRef.current.dir.y) > 0.2

      if (s.mode === 'DIG') {
        // consume digging and move
        updatePlayerDigging(s, fixedDt, joystickRef.current.dir)
        // dig terrain if moving
        if (moving) {
          const r = digAt(s.map, Math.floor(s.player.pos.x / s.config.tile), Math.floor((s.player.pos.y + 2) / s.config.tile), 2)
          if (r.dug > 0) {
            s.res.gold += r.gold
            play(220)
          }
        }
        // puzzle trigger
        if (now >= s.nextPuzzleTime) {
          s.mode = 'PUZZLE'
          puzzleRef.current.points = []
          s.nextPuzzleTime = now + 30_000
        }
        // random event
        maybeStartRandomEvent(s, now)
      }

      if (s.mode === 'EVENT') {
        if (s.event?.type === 'quake') {
          // apply quake once at start
          if (Math.floor((now - s.runStartTime) / 500) % 8 === 0) {
            applyQuake(s.map, s.rng)
          }
        }
        updateEvent(s, now)
      }

      // global resource update
      updateResources(s, fixedDt, s.mode === 'DIG' && moving)
      s.res.heat = clamp(s.res.heat + nearLavaHeat(s) * fixedDt, 0, 100)

      // fluids
      updateLava(s, fixedDt)

      // check deaths
      if (isDead(s) || now - s.runStartTime > s.runDuration) {
        s.mode = 'GAMEOVER'
        s.paused = true
        setPaused(true)
        setRunning(false)
        const score = Math.floor(s.res.gold + s.player.depth * 0.1)
        setGold(Math.floor(s.res.gold))
        if (score > highScore) setHighScore(score)
      }

      setEventLabel(s.event ? ({ quake: '地震', crash: '价格暴跌', overload: '超载风暴' } as const)[s.event.type] : null)
    }

    // draw
    draw(s, ctx)

    rafRef.current = requestAnimationFrame(loop)
  }, [highScore, play])

  function draw(s: GameState, ctx: CanvasRenderingContext2D): void {
    const w = s.config.width * dpr
    const h = s.config.height * dpr
    ctx.setTransform(1, 0, 0, 1, 0, 0)
    ctx.clearRect(0, 0, w, h)

    ctx.scale(dpr, dpr)

    // background
    ctx.fillStyle = '#0b1020'
    ctx.fillRect(0, 0, s.config.width, s.config.height)

    // camera
    const camY = s.mode === 'DIG' ? clamp(s.player.pos.y - s.config.height * 0.3, 0, s.map.h * s.config.tile - s.config.height) : 0

    // draw map tiles
    const tile = s.config.tile
    const startY = Math.floor(camY / tile)
    const endY = Math.min(s.map.h, Math.ceil((camY + s.config.height) / tile))
    for (let y = startY; y < endY; y++) {
      for (let x = 0; x < s.map.w; x++) {
        const idx = y * s.map.w + x
        const t = s.map.tiles[idx]
        if (t === 0) continue
        if (t === 1) ctx.fillStyle = '#23324a'
        if (t === 2) ctx.fillStyle = '#d4af37'
        if (t === 3) ctx.fillStyle = '#b91c1c'
        ctx.fillRect(x * tile, y * tile - camY, tile, tile)
      }
    }

    // draw ores (hook stage)
    if (s.mode === 'HOOK') {
      for (const o of s.ores) {
        ctx.beginPath()
        ctx.arc(o.pos.x, o.pos.y, o.radius, 0, Math.PI * 2)
        ctx.fillStyle = '#ffd966'
        ctx.fill()
      }
    }

    // player
    ctx.fillStyle = '#8bd3ff'
    ctx.beginPath()
    ctx.arc(s.player.pos.x, s.player.pos.y - camY, 8, 0, Math.PI * 2)
    ctx.fill()

    // hook line
    if (s.mode === 'HOOK') {
      ctx.strokeStyle = '#bfbfbf'
      ctx.lineWidth = 2
      ctx.beginPath()
      ctx.moveTo(s.player.pos.x, s.player.pos.y)
      ctx.lineTo(s.hook.head.x, s.hook.head.y)
      ctx.stroke()
      // hook head
      ctx.beginPath()
      ctx.arc(s.hook.head.x, s.hook.head.y, 5, 0, Math.PI * 2)
      ctx.fillStyle = '#93c5fd'
      ctx.fill()
    }

    // lava surface
    const lavaY = s.map.lavaLevel * tile - camY
    ctx.fillStyle = 'rgba(239,68,68,0.5)'
    ctx.fillRect(0, lavaY, s.config.width, s.config.height - lavaY)

    // overlays
    if (!unlocked) {
      ctx.font = 'bold 16px sans-serif'
      strokeText(ctx, '轻触屏幕以启用音效', 16, 26)
    }
    if (s.paused && s.mode === 'GAMEOVER') {
      ctx.font = 'bold 18px sans-serif'
      const score = Math.floor(s.res.gold + s.player.depth * 0.1)
      strokeText(ctx, `结算: 分数 ${score}`, 16, 52)
    }

    // joystick visual
    if (s.mode === 'DIG') {
      const j = joystickRef.current
      const c = { x: 64, y: s.config.height - 64 }
      ctx.strokeStyle = 'rgba(255,255,255,0.3)'
      ctx.lineWidth = 2
      ctx.beginPath()
      ctx.arc(c.x, c.y, 40, 0, Math.PI * 2)
      ctx.stroke()
      if (j.active) {
        ctx.beginPath()
        ctx.arc(c.x + j.dir.x * 24, c.y + j.dir.y * 24, 14, 0, Math.PI * 2)
        ctx.fillStyle = 'rgba(255,255,255,0.4)'
        ctx.fill()
      }
    }

    if (s.mode === 'PUZZLE') {
      ctx.font = 'bold 14px sans-serif'
      strokeText(ctx, '划一条线，开辟金块通路', 16, 52)
      const pts = puzzleRef.current.points
      if (pts.length > 1) {
        ctx.strokeStyle = '#22d3ee'
        ctx.lineWidth = 3
        ctx.beginPath()
        const p0 = pts[0]!
        ctx.moveTo(p0.x, p0.y)
        for (let i = 1; i < pts.length; i++) {
          const pi = pts[i]!
          ctx.lineTo(pi.x, pi.y)
        }
        ctx.stroke()
      }
    }
  }

  const startGame = useCallback(() => {
    if (!stateRef.current) ensureState()
    const s = stateRef.current!
    s.paused = false
    setPaused(false)
    s.runStartTime = performance.now()
    s.mode = 'HOOK'
    setRunning(true)
    if (!rafRef.current) rafRef.current = requestAnimationFrame(loop)
  }, [ensureState, loop])

  const pauseGame = useCallback(() => {
    const s = stateRef.current
    if (!s) return
    s.paused = !s.paused
    setPaused(s.paused)
  }, [])

  const restartGame = useCallback(() => {
    ensureState()
    const s = stateRef.current!
    s.paused = false
    setPaused(false)
    s.mode = 'HOOK'
    s.res.gold = 0
    s.res.heat = 0
    s.res.fuel = s.baseRes.fuel
    s.res.o2 = s.baseRes.o2
    s.runStartTime = performance.now()
    setRunning(true)
  }, [ensureState])

  const openShop = useCallback(() => setShopOpen(true), [])
  const closeShop = useCallback(() => setShopOpen(false), [])

  // canvas size management
  useEffect(() => {
    const resize = () => {
      const container = containerRef.current
      const canvas = canvasRef.current
      if (!container || !canvas) return
      // Full width, 16:9-ish height but mobile-first
      const width = container.clientWidth - 16
      const height = Math.min(Math.floor(width * 1.6), window.innerHeight - 160)
      canvas.width = Math.floor(width * dpr)
      canvas.height = Math.floor(height * dpr)
      canvas.style.width = `${width}px`
      canvas.style.height = `${height}px`
    }
    resize()
    window.addEventListener('resize', resize)
    return () => window.removeEventListener('resize', resize)
  }, [dpr])

  // RAF
  useEffect(() => {
    if (!rafRef.current) rafRef.current = requestAnimationFrame(loop)
    return () => {
      if (rafRef.current) cancelAnimationFrame(rafRef.current)
      rafRef.current = null
    }
  }, [loop])

  // pointer controls
  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const getPos = (e: PointerEvent): Vec2 => {
      const rect = canvas.getBoundingClientRect()
      return { x: (e.clientX - rect.left), y: (e.clientY - rect.top) }
    }
    const onDown = (e: PointerEvent) => {
      e.preventDefault()
      if (!unlocked) unlock()
      const s = stateRef.current
      if (!s) return
      const pos = getPos(e)
      if (s.mode === 'HOOK') {
        fireHook(s)
        play(440)
      } else if (s.mode === 'DIG') {
        // joystick area bottom-left quarter
        const center = { x: 64, y: s.config.height - 64 }
        const dx = pos.x - center.x
        const dy = pos.y - center.y
        const dist = Math.hypot(dx, dy)
        if (dist < 60) {
          joystickRef.current.active = true
          joystickRef.current.id = e.pointerId
          joystickRef.current.origin = center
          joystickRef.current.dir = { x: dx / 40, y: dy / 40 }
        }
      } else if (s.mode === 'PUZZLE') {
        puzzleRef.current.drawing = true
        puzzleRef.current.points = [pos]
      }
    }
    const onMove = (e: PointerEvent) => {
      const s = stateRef.current
      if (!s) return
      const pos = getPos(e)
      if (s.mode === 'DIG' && joystickRef.current.active && joystickRef.current.id === e.pointerId) {
        const center = joystickRef.current.origin
        const dx = pos.x - center.x
        const dy = pos.y - center.y
        const len = Math.hypot(dx, dy)
        const nx = dx / (len || 1)
        const ny = dy / (len || 1)
        joystickRef.current.dir = { x: clamp(nx * Math.min(1, len / 40), -1, 1), y: clamp(ny * Math.min(1, len / 40), -1, 1) }
      } else if (s.mode === 'PUZZLE' && puzzleRef.current.drawing) {
        puzzleRef.current.points.push(pos)
      }
    }
    const onUp = (e: PointerEvent) => {
      const s = stateRef.current
      if (!s) return
      if (s.mode === 'DIG' && joystickRef.current.id === e.pointerId) {
        joystickRef.current.active = false
        joystickRef.current.id = null
        joystickRef.current.dir = { x: 0, y: 0 }
      } else if (s.mode === 'PUZZLE' && puzzleRef.current.drawing) {
        // apply single stroke
        const pts = puzzleRef.current.points
        puzzleRef.current.drawing = false
        if (pts.length > 1) {
          for (let i = 1; i < pts.length; i++) {
            const a = pts[i - 1]!
            const b = pts[i]!
            const steps = Math.max(2, Math.floor(Math.hypot(b.x - a.x, b.y - a.y) / 4))
            for (let k = 0; k <= steps; k++) {
              const t = k / steps
              const x = a.x + (b.x - a.x) * t
              const y = a.y + (b.y - a.y) * t
              digAt(s.map, Math.floor(x / s.config.tile), Math.floor((y + 2) / s.config.tile), 1)
            }
          }
          play(520)
          vibrate(30)
        }
        s.mode = 'SHOP'
        setShopOpen(true)
      }
    }

    canvas.addEventListener('pointerdown', onDown)
    canvas.addEventListener('pointermove', onMove)
    canvas.addEventListener('pointerup', onUp)
    canvas.addEventListener('pointercancel', onUp)
    return () => {
      canvas.removeEventListener('pointerdown', onDown)
      canvas.removeEventListener('pointermove', onMove)
      canvas.removeEventListener('pointerup', onUp)
      canvas.removeEventListener('pointercancel', onUp)
    }
  }, [play, unlock, unlocked, vibrate])

  // sync gold from game state into react state for shop
  useEffect(() => {
    const id = setInterval(() => {
      const s = stateRef.current
      if (!s) return
      setGold(Math.floor(s.res.gold))
    }, 200)
    return () => clearInterval(id)
  }, [])

  // shop effects
  useEffect(() => {
    const s = stateRef.current
    if (!s) return
    s.upgrades = upgrades
  }, [upgrades])

  return (
    <div ref={containerRef} className="w-full max-w-2xl mx-auto px-2 py-4">
      <div className="text-lg font-bold mb-2">疯狂矿工 v0.1</div>
      <div className="relative">
        <MobileCanvas ref={canvasRef} />
        <HUD gold={gold} fuel={stateRef.current?.res.fuel ?? 100} o2={stateRef.current?.res.o2 ?? 100} heat={stateRef.current?.res.heat ?? 0} depth={stateRef.current?.player.depth ?? 0} eventLabel={eventLabel} highScore={highScore} />
        <Buttons running={running} paused={paused} onStart={startGame} onPause={pauseGame} onRestart={restartGame} onOpenShop={openShop} />
        <Shop open={shopOpen} onClose={() => { setShopOpen(false); const s = stateRef.current; if (s && s.mode === 'SHOP') { s.mode = 'DIG' } }} gold={gold} setGold={(g) => { setGold(g); const s = stateRef.current; if (s) s.res.gold = g }} upgrades={upgrades} setUpgrades={setUpgrades} />
      </div>
      <div className="text-xs opacity-70 mt-2 leading-relaxed">
        操作说明：抓钩阶段点击屏幕发射抓钩，命中金块获取金币；挖掘阶段使用左下角虚拟摇杆移动与挖掘；当触发解谜阶段时，单次划线开辟通路。注意燃料、氧气与温度，岩浆会随时间上升。音效将在首次触控后启用。
      </div>
    </div>
  )
}

export default MadMinerGame
