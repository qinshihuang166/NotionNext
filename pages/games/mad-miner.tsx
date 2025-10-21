import dynamic from 'next/dynamic'
import React from 'react'
import Head from 'next/head'

const MadMinerGame = dynamic(() => import('@/components/games/mad-miner/Game').then(m => m.MadMinerGame), { ssr: false })

const MadMinerPage: React.FC = () => {
  return (
    <>
      <Head>
        <title>疯狂矿工 - NotionNext</title>
        <meta name="description" content="疯狂矿工 v0.1 - 抓钩 + 挖掘 + 解谜 + 事件 的小游戏" />
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" />
      </Head>
      <div className="min-h-screen w-full flex flex-col items-center justify-start">
        <MadMinerGame />
      </div>
    </>
  )
}

export default MadMinerPage
