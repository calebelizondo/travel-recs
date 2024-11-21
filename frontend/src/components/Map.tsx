import React, { useState } from 'react';
import { ComposableMap, Geographies, Geography } from 'react-simple-maps';
import worldGeoJson from '../assets/map.json'; 
import { CountryInfo, cutoff } from '../types';

interface GeographyFeature {
  rsmKey: any;
  properties: {
    ISO_A3: string; 
  };
  geometry: {
    coordinates: any; 
  };
}

interface MapProps {
  queryResult: CountryInfo[] | null;
}

const Map: React.FC<MapProps> = ({queryResult}) => {

  const country_codes = Array.isArray(queryResult)
    ? queryResult.slice(0, cutoff).map((c: CountryInfo) => c.code)
    : [];

  console.log("country codes:", country_codes)


  return (
        <ComposableMap
            projection="geoNaturalEarth1"
            projectionConfig={{ scale: 120 }}
        >
        <Geographies geography={worldGeoJson}>
            {({ geographies }) =>
            geographies.map((geo: GeographyFeature) => {
                const isHighlighted = country_codes.includes(geo.properties.ISO_A3);  
                return (
                <Geography
                    key={geo.rsmKey}
                    geography={geo}
                    fill={isHighlighted ? '#004ba7' : '#EAEAEA'}
                    stroke="#D6D6DA"
                    strokeWidth={0.5}
                    style={{
                    default: { outline: 'none' },
                    hover: { fill: isHighlighted ? 'blue' : '#EAEAEA', transition: 'all 0.3s' },
                    }}
                />
                );
            })
            }
        </Geographies>
        </ComposableMap>
  );
}

export default Map;
