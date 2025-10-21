import BLOG from '@/blog.config'
import { siteConfig } from '@/lib/config'
import { getGlobalData } from '@/lib/db/getSiteData'
import DecompressionGame from '@/components/DecompressionGame'

/**
 * 微信小程序：解压小游戏，玩玩就上瘾了
 * 以 H5 方式提供，兼容在微信中直接打开
 */
export default function WxMiniAppDecompression(props) {
  const title = '微信小程序：解压小游戏，玩玩就上瘾了'
  return (
    <div className='px-4 md:px-6 lg:px-8 py-6 md:py-10 max-w-5xl mx-auto'>
      <h1 className='text-2xl md:text-3xl font-bold tracking-tight mb-2'>{title}</h1>
      <p className='text-gray-500 dark:text-gray-400 mb-4'>
        轻松好玩的泡泡纸解压小游戏，随点随爆，缓解压力，玩玩就上瘾。
      </p>
      <DecompressionGame rows={12} cols={8} />
    </div>
  )
}

export async function getStaticProps({ locale }) {
  const from = 'wx-miniapp-decompression'
  const props = await getGlobalData({ from, locale })

  // 提供 SEO 所需的最小字段
  props.post = {
    type: 'Post',
    title: '微信小程序：解压小游戏，玩玩就上瘾了',
    summary: '轻松好玩的泡泡纸解压小游戏（H5），随点随爆，缓解压力，玩玩就上瘾。',
    slug: 'wx-miniapp/decompression'
  }

  return {
    props,
    revalidate: siteConfig('NEXT_REVALIDATE_SECOND', BLOG.NEXT_REVALIDATE_SECOND, props.NOTION_CONFIG)
  }
}
