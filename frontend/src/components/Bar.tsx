import React from 'react';
import { CountryInfo, Filter, Climate, Cost, climateIcons, costSymbols } from "../types";
import SearchBar from "./SearchBar";
import "./styles.css";

interface BarProps {
  setQueryResult: (result: CountryInfo[] | null) => void;
  setIsLoading: (isLoading: boolean) => void;
  query: string;
  setQuery: (q: string) => void;
  filter: Filter;
  setFilter: (f: Filter) => void;
}

const Bar: React.FC<BarProps> = ({ setQueryResult, setIsLoading, query, setQuery, filter, setFilter }) => {

  const toggleClimate = (climate: Climate) => {
    setFilter({
      ...filter,
      climate: filter.climate.includes(climate)
        ? filter.climate.filter(c => c !== climate)
        : [...filter.climate, climate]
    });
  };

  const toggleCost = (cost: Cost) => {
    setFilter({
      ...filter,
      cost: filter.cost.includes(cost)
        ? filter.cost.filter(c => c !== cost)
        : [...filter.cost, cost]
    });
  };

  return (
    <div className="sticky-bar-container">
      <SearchBar setQueryResult={setQueryResult} setIsLoading={setIsLoading} query={query} setQuery={setQuery} />

      <div className="filter-buttons-container">
        <div>    
            {(['hot', 'cold', 'humid'] as Climate[]).map((climate) => (
            <button
                key={climate}
                className={`filter-button ${filter.climate.includes(climate) ? 'active' : 'inactive'}`}
                onClick={() => toggleClimate(climate)}
            >
                {climateIcons[climate]}
            </button>
            ))}
        </div>
            <div>
            {([1, 2, 3] as Cost[]).map((cost) => (
            <button
                key={cost}
                className={`filter-button ${filter.cost.includes(cost as Cost) ? 'active' : 'inactive'}`}
                onClick={() => toggleCost(cost as Cost)}
            >
                {costSymbols[cost]}
            </button>
            ))}
         </div>
      </div>
    </div>
  );
};

export default Bar;
