import { useEffect, useMemo, useRef, useState } from 'react'

/**
 * 解压泡泡纸小游戏（纯前端）
 * - 点击气泡即可“爆炸”，伴随轻微的弹跳动画与声音
 * - 支持重置、随机填充
 */
export default function DecompressionGame({ rows = 12, cols = 8 }) {
  const total = rows * cols
  const [popped, setPopped] = useState(() => new Set())
  const [pressedAt, setPressedAt] = useState({}) // 用于触发气泡动画
  const audioCtxRef = useRef(null)

  useEffect(() => {
    if (typeof window !== 'undefined' && !audioCtxRef.current) {
      try {
        const Ctx = window.AudioContext || window.webkitAudioContext
        audioCtxRef.current = Ctx ? new Ctx() : null
      } catch (e) {
        audioCtxRef.current = null
      }
    }
  }, [])

  const pop = (i) => {
    setPopped(prev => {
      if (prev.has(i)) return prev
      const next = new Set(prev)
      next.add(i)
      return next
    })
    // 触发“弹跳”动画
    setPressedAt(prev => ({ ...prev, [i]: Date.now() }))
    setTimeout(() => {
      setPressedAt(prev => {
        const n = { ...prev }
        delete n[i]
        return n
      })
    }, 160)
    playPopSound()
  }

  const isPopped = (i) => popped.has(i)

  const reset = () => {
    setPopped(new Set())
    setPressedAt({})
  }

  const randomFill = () => {
    const next = new Set()
    const count = Math.floor(total * 0.3 + Math.random() * total * 0.4) // 30%~70%
    while (next.size < count) {
      next.add(Math.floor(Math.random() * total))
    }
    setPopped(next)
  }

  const playPopSound = () => {
    const ctx = audioCtxRef.current
    if (!ctx) return
    // 使用 WebAudio 生成简短的“pop”声音
    const o = ctx.createOscillator()
    const g = ctx.createGain()
    o.type = 'square'
    o.frequency.setValueAtTime(440 + Math.random() * 220, ctx.currentTime)
    g.gain.setValueAtTime(0.0001, ctx.currentTime)
    g.gain.exponentialRampToValueAtTime(0.2, ctx.currentTime + 0.01)
    g.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.09)
    o.connect(g)
    g.connect(ctx.destination)
    o.start()
    o.stop(ctx.currentTime + 0.1)
  }

  const cells = useMemo(() => Array.from({ length: total }, (_, i) => i), [total])

  return (
    <div className='w-full flex flex-col items-center select-none'>
      <div className='w-full max-w-3xl flex items-center justify-between mt-4 mb-3 px-2'>
        <div className='text-sm text-gray-500 dark:text-gray-400'>
          已捏爆 {popped.size} / {total}
        </div>
        <div className='space-x-2'>
          <button onClick={randomFill} className='px-3 py-1 text-sm rounded-md bg-indigo-600 hover:bg-indigo-500 text-white'>随机填充</button>
          <button onClick={reset} className='px-3 py-1 text-sm rounded-md bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-900 dark:text-gray-100'>重置</button>
        </div>
      </div>

      <div className='grid gap-3 p-4 rounded-2xl bg-gradient-to-br from-gray-50 to-gray-200 dark:from-[#0b0d14] dark:to-[#111827] shadow-inner'
           style={{ gridTemplateColumns: `repeat(${cols}, minmax(0, 1fr))` }}>
        {cells.map((i) => {
          const poppedNow = isPopped(i)
          const bounce = !!pressedAt[i]
          return (
            <button
              key={i}
              onClick={() => pop(i)}
              aria-label={poppedNow ? '已捏爆' : '未捏'}
              className={`relative w-16 h-16 md:w-20 md:h-20 rounded-full transition-all duration-100 outline-none focus:outline-none active:scale-95 ${poppedNow ? 'bg-gradient-to-br from-gray-300 to-gray-400 dark:from-gray-600 dark:to-gray-700' : 'bg-gradient-to-br from-pink-200 to-pink-300 dark:from-pink-500 dark:to-pink-600'} ${bounce ? 'scale-95' : ''}`}
            >
              <span className={`absolute inset-0 rounded-full ${poppedNow ? 'shadow-inner shadow-black/40' : 'shadow-lg shadow-pink-400/40 dark:shadow-black/40'}`} />
              {!poppedNow && (
                <span className='absolute inset-0 rounded-full bg-white/30 dark:bg-white/10 blur-md pointer-events-none' />
              )}
            </button>
          )
        })}
      </div>

      <p className='mt-4 text-gray-500 dark:text-gray-400 text-sm'>
        小提示：点击气泡解压放松，玩玩就上瘾了 😄
      </p>
    </div>
  )
}
