export type Climate = 'hot' | 'cold' | 'humid' | "dry" | "mild";
export type Cost = 1 | 2 | 3;


export interface Filter {
  climate: Climate[],
  cost: Cost[]
};

export interface CountryInfo {
    name: string, 
    code: string, 
    score: number, 
    info: {
      bio: string
      climate: Climate[], 
      cost: Cost
    } 
}

export const cutoff = 12;
