import React from 'react'

type ButtonsProps = {
  running: boolean
  paused: boolean
  onStart: () => void
  onPause: () => void
  onRestart: () => void
  onOpenShop: () => void
}

export const Buttons: React.FC<ButtonsProps> = ({ running, paused, onStart, onPause, onRestart, onOpenShop }) => {
  return (
    <div className="fixed bottom-3 left-1/2 -translate-x-1/2 flex gap-3 z-20">
      {!running && (
        <button className="px-4 py-2 rounded bg-emerald-500 text-white shadow" onClick={onStart}>
          开始
        </button>
      )}
      {running && (
        <>
          <button className="px-4 py-2 rounded bg-amber-500 text-white shadow" onClick={onPause}>
            {paused ? '继续' : '暂停'}
          </button>
          <button className="px-4 py-2 rounded bg-rose-600 text-white shadow" onClick={onRestart}>
            重开
          </button>
          <button className="px-4 py-2 rounded bg-sky-600 text-white shadow" onClick={onOpenShop}>
            商店
          </button>
        </>
      )}
    </div>
  )
}
