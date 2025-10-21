export class RNG {
  private seed: number
  constructor(seed: number = Date.now() % 2147483647) {
    if (seed <= 0) seed += 2147483646
    this.seed = seed
  }
  next(): number {
    this.seed = (this.seed * 48271) % 2147483647
    return this.seed
  }
  nextFloat(): number {
    return (this.next() - 1) / 2147483646
  }
  range(min: number, max: number): number {
    return min + this.nextFloat() * (max - min)
  }
  int(min: number, max: number): number {
    return Math.floor(this.range(min, max + 1))
  }
  pick<T>(arr: T[]): T {
    return arr[Math.floor(this.nextFloat() * arr.length)] as T
  }
}
