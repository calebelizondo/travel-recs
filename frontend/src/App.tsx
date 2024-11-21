import React, { useState, useEffect, useRef } from 'react';
import LandingPage from './pages/LandingPage'; 
import MapPage from './pages/MapPage';  
import Bar from './components/Bar';
import { CountryInfo, Filter } from './types';
import ResultsPage from './pages/ResultsPage';
import "./styles.css";

function App() {
  const [queryResult, setQueryResult] = useState<CountryInfo[] | null>(null);
  const [filter, setFilter] = useState<Filter>({climate: ['humid', 'hot', 'cold'], cost: [1, 2, 3]});
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const targetDivRef = useRef<HTMLDivElement | null>(null); 
  const [showStickyBar, setShowStickyBar] = useState<boolean>(false);

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

  const handleScroll = () => {
    if (window.scrollY > 100) {  
      setShowStickyBar(true);
    } else {
      setShowStickyBar(false);
    }
  };

  useEffect(() => {
    window.addEventListener('scroll', handleScroll);
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);


  const filteredQueryResults: CountryInfo[] = [];
  if (queryResult) queryResult.forEach((c: CountryInfo) => {
    if (filter.cost.includes(c.info.cost)) filteredQueryResults.push(c);
  });

  return (
    <>
      <div className={`sticky-bar ${showStickyBar ? 'visible' : ''}`}>
        <Bar setQueryResult={setQueryResult} setIsLoading={setIsLoading} />
      </div>
      <LandingPage setQueryResult={setQueryResult} setIsLoading={setIsLoading}/>
      <MapPage queryResult={filteredQueryResults} targetDiv={targetDivRef} isLoading={isLoading}/>
      <ResultsPage queryResult={filteredQueryResults}></ResultsPage>
    </>
  );
}

export default App;
