
import { siteConfig } from '@/lib/config'
import { loadExternalResource } from '@/lib/utils'
import { useEffect } from 'react'

/**
 * Google AdSense Pop-up ad
 * @returns
 */
const GoogleAdsensePopup = () => {
  const ADSENSE_GOOGLE_ID = siteConfig('ADSENSE_GOOGLE_ID')

  useEffect(() => {
    if (ADSENSE_GOOGLE_ID) {
      loadExternalResource(`https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${ADSENSE_GOOGLE_ID}`, 'js').then(url => {
        console.log('Load Google AdSense Pop-up success.')
        const adsbygoogle = window.adsbygoogle || []
        adsbygoogle.push({})
      })
    }
  }, [])

  const handleClick = () => {
    const adsbygoogle = window.adsbygoogle || []
    adsbygoogle.push({})
  }

  if (!ADSENSE_GOOGLE_ID) {
    return null
  }

  return (
    <div className='fixed bottom-0 left-0 w-full z-50'>
      <div className='container mx-auto p-4 text-center'>
        <button
          onClick={handleClick}
          className='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded'
        >
          Show Ad
        </button>
      </div>
    </div>
  )
}

export default GoogleAdsensePopup
