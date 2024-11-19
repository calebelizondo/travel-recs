import React, { useState } from 'react';
import { ComposableMap, Geographies, Geography } from 'react-simple-maps';
import worldGeoJson from '../assets/map.json'; 

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

}

const Map: React.FC<MapProps> = () => {
  const [highlightedCountries, setHighlightedCountries] = useState<string[]>(['USA', 'CAN']); 

  return (
        <ComposableMap
            projection="geoNaturalEarth1"
            projectionConfig={{ scale: 150 }}
        >
        <Geographies geography={worldGeoJson}>
            {({ geographies }) =>
            geographies.map((geo: GeographyFeature) => {
                const isHighlighted = highlightedCountries.includes(geo.properties.ISO_A3);  
                console.log(isHighlighted);
                return (
                <Geography
                    key={geo.rsmKey}
                    geography={geo}
                    fill={isHighlighted ? 'orange' : '#EAEAEA'}
                    stroke="#D6D6DA"
                    strokeWidth={0.5}
                    style={{
                    default: { outline: 'none' },
                    hover: { fill: 'blue', transition: 'all 0.3s' },
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
