// ----------------------
// File: src/utils/burnoutForecast.ts
// ----------------------

export function getBurnoutForecast(burnoutScores: number[], threshold = 80): number | null {
    const deltas = burnoutScores.slice(1).map((val, i) => val - burnoutScores[i]);
    const avgRate = deltas.reduce((a, b) => a + b, 0) / deltas.length;
    const current = burnoutScores[burnoutScores.length - 1];
  
    if (avgRate <= 0) return null;  // No increasing trend
  
    const daysToBurnout = (threshold - current) / avgRate;
    return daysToBurnout > 0 ? Math.ceil(daysToBurnout) : 0;
  }