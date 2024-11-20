import React, { useState, useEffect, useRef } from 'react';
import LandingPage from './pages/LandingPage'; 
import MapPage from './pages/MapPage';  
import { CountryInfo } from './types';
import ResultsPage from './pages/ResultsPage';

function App() {
  const [queryResult, setQueryResult] = useState<CountryInfo[] | null>(null);
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
    if (queryResult) {
      targetDivRef.current?.scrollIntoView({
        behavior: 'smooth',
        block: 'center',
      });
    }
  }, [queryResult]); 

  return (
    <>
      <LandingPage setQueryResult={setQueryResult} setIsLoading={setIsLoading}/>
      <MapPage queryResult={queryResult} targetDiv={targetDivRef} isLoading={isLoading}/>
      <ResultsPage queryResults={queryResult}></ResultsPage>
    </>
  );
}

export default App;
