export interface Employee {
    id: string;
    name: string;
    department: string;
    role: string;
    productivityScore: number;
    burnoutScore: number;
    burnoutHistory: number[];
    lastActive: string;
    goalsCompleted: number;
    goalsTotal: number;
    suggestions: string[];
    status: string;
    daysToBurnout: number;
  }