import React, { useState, useEffect, useRef } from 'react';
import LandingPage from './pages/LandingPage';
import MapPage from './pages/MapPage';
import Bar from './components/Bar';
import { CountryInfo, Filter } from './types';
import ResultsPage from './pages/ResultsPage';
import "./styles.css";

function App() {
  const [query, setQuery] = useState<string>('');
  const [queryResult, setQueryResult] = useState<CountryInfo[] | null>(null);
  const [filter, setFilter] = useState<Filter>({ climate: ['humid', 'hot', 'cold'], cost: [1, 2, 3] });
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const targetDivRef = useRef<HTMLDivElement | null>(null);
  const [showStickyBar, setShowStickyBar] = useState<boolean>(false);

  useEffect(() => {
    targetDivRef.current?.scrollIntoView({
      behavior: 'smooth',
      block: 'center',
    });
  }, [isLoading]);

  useEffect(() => {
    setIsLoading(false);
    if (queryResult) {
      targetDivRef.current?.scrollIntoView({
        behavior: 'smooth',
        block: 'center',
      });
    }
  }, [queryResult]);

  const handleScroll = () => {
    console.log("scrolling ...");
    console.log(window.scrollY);
    if (window.scrollY > 300) {
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
  if (queryResult) {
    queryResult.forEach((c: CountryInfo) => {
      const hasCostMatch = filter.cost.includes(c.info.cost);
      const hasClimateMatch =
        !c.info.climate || c.info.climate.length === 0 || c.info.climate.some((climate) => filter.climate.includes(climate));
      
      if (hasCostMatch && hasClimateMatch) {
        filteredQueryResults.push(c);
      }
    });
  }

  return (
    <>
      { showStickyBar ? (
        <div className={`sticky-bar ${showStickyBar ? 'visible' : ''}`}>
          <Bar setQueryResult={setQueryResult} setIsLoading={setIsLoading} query={query} setQuery={setQuery} filter={filter} setFilter={setFilter}/>
        </div>
      ) : (
        <></>
      )}
        
      <LandingPage setQueryResult={setQueryResult} setIsLoading={setIsLoading} query={query} setQuery={setQuery}/>
      <MapPage queryResult={filteredQueryResults} targetDiv={targetDivRef} isLoading={isLoading} />
      <ResultsPage queryResult={filteredQueryResults}></ResultsPage>
    </>
  );
}

export default App;
