export function predictBurnoutDays(history: number[], threshold = 75): number {
    if (history.length < 2) return -1;
  
    const recent = history.slice(-5); // last 5 scores
    const diffs = recent.slice(1).map((score, i) => score - recent[i]);
    const avgRate = diffs.reduce((a, b) => a + b, 0) / diffs.length;
  
    const current = recent[recent.length - 1];
  
    if (avgRate <= 0) return Infinity; // no rising trend
  
    const daysLeft = Math.ceil((threshold - current) / avgRate);
    return daysLeft > 0 ? daysLeft : 0;
  }