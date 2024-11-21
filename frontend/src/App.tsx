import React, { useState, useEffect, useRef } from 'react';
import LandingPage from './pages/LandingPage'; 
import MapPage from './pages/MapPage';  
import { CountryInfo, Filter } from './types';
import ResultsPage from './pages/ResultsPage';

function App() {
  const [queryResult, setQueryResult] = useState<CountryInfo[] | null>(null);
  const [filter, setFilter] = useState<Filter>({climate: ['humid', 'hot', 'cold'], cost: [1, 2, 3]});
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const targetDivRef = useRef<HTMLDivElement | null>(null); 

  useEffect(() => {
    targetDivRef.current?.scrollIntoView({
      behavior: 'smooth',
      block: 'center',
    });
  }, [isLoading])

  useEffect(() => {
    setIsLoading(false);
    console.log(queryResult);
    if (queryResult) {
      targetDivRef.current?.scrollIntoView({
        behavior: 'smooth',
        block: 'center',
      });
    }
  }, [queryResult]); 

  const filteredQueryResults: CountryInfo[] = [];
  if (queryResult) queryResult.forEach((c: CountryInfo) => {
    if (filter.cost.includes(c.info.cost)) filteredQueryResults.push(c);
  });

  return (
    <>
      <LandingPage setQueryResult={setQueryResult} setIsLoading={setIsLoading}/>
      <MapPage queryResult={filteredQueryResults} targetDiv={targetDivRef} isLoading={isLoading}/>
      <ResultsPage queryResult={filteredQueryResults}></ResultsPage>
    </>
  );
}

export default App;
