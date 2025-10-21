import { RNG } from '../utils/random'
import { Upgrades } from '../storage/save'

export type Vec2 = { x: number, y: number }

export type Resources = {
  gold: number
  fuel: number
  o2: number
  heat: number
}

export type Player = {
  pos: Vec2
  vel: Vec2
  angle: number // for hook rotation
  depth: number
}

export type HookState = {
  rotating: boolean
  angle: number
  speed: number
  ropeLen: number
  fired: boolean
  head: Vec2
  target?: Ore | null
  returning: boolean
  magnetizing: boolean
}

export type Ore = {
  id: number
  pos: Vec2
  vel: Vec2
  radius: number
  value: number
  weight: number
  type: 'gold' | 'bomb' | 'toxic' | 'mag'
}

export type EventType = 'quake' | 'crash' | 'overload'
export type ActiveEvent = {
  type: EventType
  endsAt: number
  priceMul: number
  digSpeedMul: number
  heatRateMul: number
}

export type MapTile = 0 | 1 | 2 | 3 // 0 air, 1 rock, 2 gold, 3 lava

export type TileMap = {
  w: number
  h: number
  tiles: MapTile[] // row-major
  lavaLevel: number // y index of lava top
}

export type GameMode = 'HOOK' | 'DIG' | 'PUZZLE' | 'EVENT' | 'SHOP' | 'PAUSE' | 'GAMEOVER'

export type GameConfig = {
  width: number
  height: number
  tile: number
}

export type GameState = {
  mode: GameMode
  time: number
  rng: RNG
  res: Resources
  baseRes: Resources
  player: Player
  hook: HookState
  ores: Ore[]
  map: TileMap
  upgrades: Upgrades
  event: ActiveEvent | null
  highScore: number
  runStartTime: number
  runDuration: number
  paused: boolean
  soundUnlocked: boolean
  config: GameConfig
  nextPuzzleTime: number
}

export const initialResources = (): Resources => ({ gold: 0, fuel: 100, o2: 100, heat: 0 })

export const createInitialState = (config: GameConfig, upgrades: Upgrades, highScore: number, seed?: number): GameState => {
  const rng = new RNG(seed ?? Date.now())
  const player: Player = { pos: { x: config.width / 2, y: config.height * 0.2 }, vel: { x: 0, y: 0 }, angle: 0, depth: 0 }
  const hook: HookState = { rotating: true, angle: -Math.PI / 3, speed: 1.2, ropeLen: 0, fired: false, head: { x: player.pos.x, y: player.pos.y }, returning: false, magnetizing: false, target: null }
  const map: TileMap = { w: Math.floor(config.width / config.tile), h: Math.floor(config.height / config.tile) * 5, tiles: [], lavaLevel: Math.floor(config.height / config.tile) * 5 }
  // Fill map with rock and some gold near surface
  map.tiles = new Array(map.w * map.h).fill(1) as MapTile[]
  for (let y = 0; y < map.h; y++) {
    for (let x = 0; x < map.w; x++) {
      const idx = y * map.w + x
      if (y < 6) map.tiles[idx] = 0 // air near top
      if (rng.nextFloat() < Math.max(0, 0.05 - y * 0.0005)) map.tiles[idx] = 2
    }
  }
  const ores: Ore[] = []
  for (let i = 0; i < 6; i++) {
    ores.push({ id: i + 1, pos: { x: rng.range(20, config.width - 20), y: rng.range(60, 140) }, vel: { x: 0, y: 0 }, radius: rng.range(8, 14), value: 10 + rng.int(0, 20), weight: rng.range(1, 3), type: 'gold' })
  }
  return {
    mode: 'HOOK',
    time: 0,
    rng,
    res: initialResources(),
    baseRes: initialResources(),
    player,
    hook,
    ores,
    map,
    upgrades,
    event: null,
    highScore,
    runStartTime: 0,
    runDuration: 90_000, // 90 seconds target
    paused: false,
    soundUnlocked: false,
    config,
    nextPuzzleTime: 0
  }
}

export const indexOf = (map: TileMap, x: number, y: number): number => y * map.w + x
export const getTile = (map: TileMap, x: number, y: number): MapTile => {
  if (x < 0 || y < 0 || x >= map.w || y >= map.h) return 1
  return map.tiles[indexOf(map, x, y)] as MapTile
}
export const setTile = (map: TileMap, x: number, y: number, t: MapTile): void => {
  if (x < 0 || y < 0 || x >= map.w || y >= map.h) return
  map.tiles[indexOf(map, x, y)] = t
}
