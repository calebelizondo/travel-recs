export type Climate = 'hot' | 'cold' | 'humid';
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

export const climateIcons: { [key in Climate]: string } = {
  hot: "🌞",
  cold: "❄️",
  humid: "💧"
};

export const costSymbols: { [key in Cost]: string } = {
  1: "$",
  2: "$$",
  3: "$$$",
};
