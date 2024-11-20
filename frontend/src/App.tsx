import React, { useState, useEffect, useRef } from 'react';
import LandingPage from './pages/LandingPage'; 
import MapPage from './pages/MapPage';  
import { CountryInfo } from './types';

function App() {
  const [queryResult, setQueryResult] = useState<CountryInfo[] | null>(null);
  const targetDivRef = useRef<HTMLDivElement | null>(null); 

  useEffect(() => {

    console.log("result:", queryResult)
    if (queryResult) {
      targetDivRef.current?.scrollIntoView({
        behavior: 'smooth',
        block: 'center',
      });
    }
  }, [queryResult]); 
  return (
    <>
      <LandingPage setQueryResult={setQueryResult} />
      <MapPage queryResult={queryResult} targetDiv={targetDivRef}/>
    </>
  );
}

export default App;
