import { RNG } from '../utils/random'
import { MapTile, TileMap, setTile, getTile } from './state'

export function generateCave(map: TileMap, rng: RNG): void {
  // Simple cellular automata / perlin-less rough caves
  for (let y = 6; y < map.h; y++) {
    for (let x = 0; x < map.w; x++) {
      const idx = y * map.w + x
      const depth = y / map.h
      let t: MapTile = 1
      const noise = rng.nextFloat()
      if (noise < 0.06 - depth * 0.02) t = 2 // gold chance decreases with depth
      if (noise > 0.9) t = 0 // air pocket
      map.tiles[idx] = t
    }
  }
  // Keep top rows open
  for (let y = 0; y < 6; y++) {
    for (let x = 0; x < map.w; x++) {
      map.tiles[y * map.w + x] = 0
    }
  }
}

export function digAt(map: TileMap, cx: number, cy: number, radius: number): { gold: number; dug: number } {
  let gold = 0
  let dug = 0
  const r2 = radius * radius
  for (let y = Math.floor(cy - radius); y <= Math.ceil(cy + radius); y++) {
    for (let x = Math.floor(cx - radius); x <= Math.ceil(cx + radius); x++) {
      const dx = x + 0.5 - cx
      const dy = y + 0.5 - cy
      if (dx * dx + dy * dy <= r2) {
        const t = getTile(map, x, y)
        if (t === 1 || t === 2) {
          if (t === 2) gold += 5
          setTile(map, x, y, 0)
          dug++
        }
      }
    }
  }
  return { gold, dug }
}

export function applyQuake(map: TileMap, rng: RNG): void {
  // Randomly open some spaces vertically
  const columns = 2 + rng.int(0, Math.max(1, Math.floor(map.w / 6)))
  for (let i = 0; i < columns; i++) {
    const x = rng.int(1, map.w - 2)
    const height = rng.int(6, Math.floor(map.h / 2))
    const start = rng.int(6, map.h - height - 1)
    for (let y = start; y < start + height; y++) {
      setTile(map, x, y, 0)
    }
  }
}

export function riseLava(map: TileMap, amount: number): void {
  map.lavaLevel = Math.max(0, map.lavaLevel - amount)
  // convert tiles below lava to lava
  for (let y = map.lavaLevel; y < map.h; y++) {
    for (let x = 0; x < map.w; x++) {
      setTile(map, x, y, 3)
    }
  }
}
