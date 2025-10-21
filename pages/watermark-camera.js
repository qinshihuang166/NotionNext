import BLOG from '@/blog.config'
import { siteConfig } from '@/lib/config'
import { getGlobalData } from '@/lib/db/getSiteData'
import { useEffect, useMemo, useRef, useState } from 'react'

const positions = [
  { value: 'bottom-left', label: '左下' },
  { value: 'bottom-right', label: '右下' },
  { value: 'top-left', label: '左上' },
  { value: 'top-right', label: '右上' }
]

const formatDateTimeLocal = date => {
  const pad = n => String(n).padStart(2, '0')
  const y = date.getFullYear()
  const m = pad(date.getMonth() + 1)
  const d = pad(date.getDate())
  const hh = pad(date.getHours())
  const mm = pad(date.getMinutes())
  return `${y}-${m}-${d} ${hh}:${mm}`
}

const WatermarkCamera = props => {
  const videoRef = useRef(null)
  const canvasRef = useRef(null)
  const streamRef = useRef(null)

  const [ready, setReady] = useState(false)
  const [facingMode, setFacingMode] = useState('environment')
  const [address, setAddress] = useState('')
  const [weather, setWeather] = useState('晴')
  const [dateTime, setDateTime] = useState(formatDateTimeLocal(new Date()))
  const [position, setPosition] = useState('bottom-left')
  const [fontSize, setFontSize] = useState(20)
  const [textColor, setTextColor] = useState('white')
  const [error, setError] = useState(null)
  const [captured, setCaptured] = useState(null)

  const isClient = useMemo(() => typeof window !== 'undefined', [])

  const startCamera = async mode => {
    try {
      setError(null)
      const constraints = {
        video: {
          facingMode: { ideal: mode || facingMode },
          width: { ideal: 1920 },
          height: { ideal: 1080 }
        },
        audio: false
      }
      const stream = await navigator.mediaDevices.getUserMedia(constraints)
      streamRef.current = stream
      if (videoRef.current) {
        videoRef.current.srcObject = stream
        await videoRef.current.play()
        setReady(true)
      }
    } catch (e) {
      console.error(e)
      setError('无法访问摄像头，请检查浏览器权限设置。')
      setReady(false)
    }
  }

  const stopCamera = () => {
    try {
      const stream = streamRef.current
      if (stream) {
        stream.getTracks().forEach(t => t.stop())
        streamRef.current = null
      }
      if (videoRef.current) {
        videoRef.current.srcObject = null
      }
      setReady(false)
    } catch (e) {
      console.error(e)
    }
  }

  const flipCamera = async () => {
    const newMode = facingMode === 'environment' ? 'user' : 'environment'
    setFacingMode(newMode)
    stopCamera()
    await startCamera(newMode)
  }

  const useNow = () => setDateTime(formatDateTimeLocal(new Date()))

  const useGeoLocation = () => {
    if (!navigator.geolocation) return
    navigator.geolocation.getCurrentPosition(
      pos => {
        const { latitude, longitude } = pos.coords
        setAddress(`纬度: ${latitude.toFixed(5)} 经度: ${longitude.toFixed(5)}`)
      },
      () => setError('无法获取定位，可手动输入地址')
    )
  }

  useEffect(() => {
    if (!isClient) return
    startCamera(facingMode)
    return () => stopCamera()
  }, [isClient])

  const renderOverlayPreview = () => {
    const isWhite = textColor === 'white'
    const bg = isWhite ? 'bg-black/40 text-white' : 'bg-white/60 text-black'
    const style = { fontSize: `${fontSize}px`, lineHeight: 1.3 }
    const text = (
      <div className={`px-3 py-1 rounded-md ${bg}`} style={style}>
        <div>{address || '地址可编辑'}</div>
        <div>{weather || '天气可编辑'}</div>
        <div>{dateTime}</div>
      </div>
    )

    const container = 'absolute m-3'
    if (position === 'bottom-left') return <div className={`${container} left-0 bottom-0`}>{text}</div>
    if (position === 'bottom-right') return <div className={`${container} right-0 bottom-0`}>{text}</div>
    if (position === 'top-left') return <div className={`${container} left-0 top-0`}>{text}</div>
    return <div className={`${container} right-0 top-0`}>{text}</div>
  }

  const capture = () => {
    try {
      const video = videoRef.current
      const canvas = canvasRef.current
      if (!video || !canvas) return

      const width = video.videoWidth || 1920
      const height = video.videoHeight || 1080
      canvas.width = width
      canvas.height = height

      const ctx = canvas.getContext('2d')
      // 绘制画面
      ctx.drawImage(video, 0, 0, width, height)

      // 水印文本
      const lines = [address, weather, dateTime].filter(Boolean)
      const padding = 16
      const lineGap = 6
      ctx.font = `${fontSize}px system-ui, -apple-system, Segoe UI, Roboto, Arial`
      ctx.textBaseline = 'top'

      // 计算背景框尺寸
      const metrics = lines.map(l => ctx.measureText(l))
      const textWidth = Math.max(...metrics.map(m => m.width))
      const textHeight = lines.length * fontSize + (lines.length - 1) * lineGap

      let x = padding
      let y = padding
      if (position.includes('right')) x = width - textWidth - padding * 2
      if (position.includes('bottom')) y = height - textHeight - padding * 2

      // 背景框
      const bgColor = textColor === 'white' ? 'rgba(0,0,0,0.45)' : 'rgba(255,255,255,0.55)'
      ctx.fillStyle = bgColor
      ctx.fillRect(x - padding, y - padding, textWidth + padding * 2, textHeight + padding * 2)

      // 文本
      ctx.fillStyle = textColor
      ctx.strokeStyle = textColor === 'white' ? 'rgba(0,0,0,0.6)' : 'rgba(255,255,255,0.8)'
      ctx.lineWidth = 2

      lines.forEach((l, i) => {
        const ty = y + i * (fontSize + lineGap)
        // 先描边增强可读性
        ctx.strokeText(l, x, ty)
        ctx.fillText(l, x, ty)
      })

      const data = canvas.toDataURL('image/jpeg', 0.95)
      setCaptured(data)
    } catch (e) {
      console.error(e)
      setError('捕获失败，请重试。')
    }
  }

  const download = () => {
    if (!captured) return
    const a = document.createElement('a')
    a.href = captured
    a.download = `watermark_${Date.now()}.jpg`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
  }

  return (
    <div className='w-full'>
      <div className='mb-5 flex items-center justify-between'>
        <h1 className='text-2xl font-bold dark:text-gray-200'>水印相机</h1>
        <div className='text-sm text-gray-500 dark:text-gray-400'>地址、天气、时间支持自由编辑</div>
      </div>

      <div className='grid md:grid-cols-3 gap-5'>
        <div className='md:col-span-2'>
          <div className='relative rounded-lg overflow-hidden bg-black'>
            <video
              ref={videoRef}
              playsInline
              muted
              autoPlay
              className={`${facingMode === 'user' ? 'scale-x-[-1]' : ''} w-full h-auto object-contain aspect-video bg-black`}
            />
            {ready && renderOverlayPreview()}
          </div>

          <div className='mt-3 flex flex-wrap gap-2'>
            <button
              onClick={capture}
              className='px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700'>
              拍照并生成水印
            </button>
            <button
              onClick={flipCamera}
              className='px-3 py-2 rounded bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-100 dark:hover:bg-gray-600'>
              切换镜头
            </button>
            <button
              onClick={useNow}
              className='px-3 py-2 rounded bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-100 dark:hover:bg-gray-600'>
              使用当前时间
            </button>
            <button
              onClick={useGeoLocation}
              className='px-3 py-2 rounded bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-100 dark:hover:bg-gray-600'>
              使用当前位置
            </button>
            {ready ? (
              <button
                onClick={stopCamera}
                className='px-3 py-2 rounded bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-100 dark:hover:bg-gray-600'>
                停止相机
              </button>
            ) : (
              <button
                onClick={() => startCamera(facingMode)}
                className='px-3 py-2 rounded bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-100 dark:hover:bg-gray-600'>
                启动相机
              </button>
            )}
          </div>

          {error && (
            <div className='mt-3 p-3 rounded bg-red-50 text-red-600 border border-red-200 text-sm'>
              {error}
            </div>
          )}

          {captured && (
            <div className='mt-5'>
              <div className='flex items-center justify-between mb-2'>
                <div className='font-medium dark:text-gray-200'>预览</div>
                <div className='flex gap-2'>
                  <button
                    onClick={download}
                    className='px-3 py-2 rounded bg-green-600 text-white hover:bg-green-700'>
                    下载图片
                  </button>
                  <button
                    onClick={() => setCaptured(null)}
                    className='px-3 py-2 rounded bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-100 dark:hover:bg-gray-600'>
                    重新拍摄
                  </button>
                </div>
              </div>
              <img src={captured} alt='captured' className='w-full rounded-lg shadow' />
            </div>
          )}

          <canvas ref={canvasRef} className='hidden' />
        </div>

        <div className='md:col-span-1'>
          <div className='p-4 rounded-lg bg-white dark:bg-hexo-black-gray shadow'>
            <div className='text-lg font-medium mb-4 dark:text-gray-200'>水印信息</div>

            <label className='block text-sm text-gray-600 dark:text-gray-300 mb-1'>地址</label>
            <input
              type='text'
              value={address}
              onChange={e => setAddress(e.target.value)}
              placeholder='例如：广东省深圳市南山区'
              className='w-full px-3 py-2 rounded border dark:bg-gray-800 dark:border-gray-700 dark:text-gray-100'
            />

            <label className='block text-sm text-gray-600 dark:text-gray-300 mt-4 mb-1'>天气</label>
            <input
              type='text'
              value={weather}
              onChange={e => setWeather(e.target.value)}
              placeholder='例如：晴 28℃'
              className='w-full px-3 py-2 rounded border dark:bg-gray-800 dark:border-gray-700 dark:text-gray-100'
            />

            <label className='block text-sm text-gray-600 dark:text-gray-300 mt-4 mb-1'>时间</label>
            <input
              type='text'
              value={dateTime}
              onChange={e => setDateTime(e.target.value)}
              placeholder='例如：2025-01-01 12:00'
              className='w-full px-3 py-2 rounded border dark:bg-gray-800 dark:border-gray-700 dark:text-gray-100'
            />

            <div className='mt-4 grid grid-cols-2 gap-3'>
              <div>
                <label className='block text-sm text-gray-600 dark:text-gray-300 mb-1'>位置</label>
                <select
                  value={position}
                  onChange={e => setPosition(e.target.value)}
                  className='w-full px-3 py-2 rounded border dark:bg-gray-800 dark:border-gray-700 dark:text-gray-100'>
                  {positions.map(p => (
                    <option key={p.value} value={p.value}>{p.label}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className='block text-sm text-gray-600 dark:text-gray-300 mb-1'>字号</label>
                <input
                  type='range'
                  min='12'
                  max='40'
                  value={fontSize}
                  onChange={e => setFontSize(parseInt(e.target.value))}
                  className='w-full'
                />
                <div className='text-xs text-gray-500 dark:text-gray-400 mt-1'>{fontSize}px</div>
              </div>
            </div>

            <div className='mt-4'>
              <label className='block text-sm text-gray-600 dark:text-gray-300 mb-1'>文字颜色</label>
              <div className='flex gap-3'>
                <label className='flex items-center gap-2 cursor-pointer'>
                  <input
                    type='radio'
                    name='textColor'
                    value='white'
                    checked={textColor === 'white'}
                    onChange={() => setTextColor('white')}
                  />
                  <span className='text-sm dark:text-gray-300'>白色</span>
                </label>
                <label className='flex items-center gap-2 cursor-pointer'>
                  <input
                    type='radio'
                    name='textColor'
                    value='black'
                    checked={textColor === 'black'}
                    onChange={() => setTextColor('black')}
                  />
                  <span className='text-sm dark:text-gray-300'>黑色</span>
                </label>
              </div>
            </div>

            <div className='mt-6 text-xs text-gray-500 dark:text-gray-400 leading-6'>
              温馨提示：
              <ul className='list-disc ml-4'>
                <li>地址、天气与时间均可自由修改。</li>
                <li>如需真实定位，可点击“使用当前位置”。</li>
                <li>如相机无法打开，请检查浏览器权限设置。</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export async function getStaticProps({ locale }) {
  const props = await getGlobalData({ from: 'watermark-camera', locale })
  return {
    props,
    revalidate: process.env.EXPORT
      ? undefined
      : siteConfig('NEXT_REVALIDATE_SECOND', BLOG.NEXT_REVALIDATE_SECOND, props.NOTION_CONFIG)
  }
}

export default WatermarkCamera
