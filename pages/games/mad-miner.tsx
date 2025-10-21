import dynamic from 'next/dynamic'
import React from 'react'
import Head from 'next/head'

const MadMinerGame = dynamic(() => import('@/components/games/mad-miner/Game').then(m => m.MadMinerGame), {
  ssr: false,
  loading: () => (
    <div className="min-h-screen w-full flex items-center justify-center text-sm opacity-70">
      正在加载游戏...
    </div>
  )
})

class ErrorBoundary extends React.Component<{ children: React.ReactNode }, { hasError: boolean }> {
  constructor(props: any) {
    super(props)
    this.state = { hasError: false }
  }
  static getDerivedStateFromError() {
    return { hasError: true }
  }
  componentDidCatch() {}
  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen w-full flex flex-col items-center justify-center gap-3 p-4">
          <div className="text-red-600">游戏初始化失败</div>
          <button
            className="px-4 py-2 rounded bg-blue-600 text-white"
            onClick={() => {
              if (typeof window !== 'undefined') window.location.reload()
            }}
          >
            重试
          </button>
        </div>
      )
    }
    return this.props.children as any
  }
}

const MadMinerPage: React.FC = () => {
  return (
    <>
      <Head>
        <title>疯狂矿工 - NotionNext</title>
        <meta name="description" content="疯狂矿工 v0.1 - 抓钩 + 挖掘 + 解谜 + 事件 的小游戏" />
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" />
      </Head>
      <div className="min-h-screen w-full flex flex-col items-center justify-start">
        <ErrorBoundary>
          <MadMinerGame />
        </ErrorBoundary>
      </div>
    </>
  )
}

export default MadMinerPage
