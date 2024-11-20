import { RefObject } from "react";
import Map from "../components/Map";
import { CountryInfo } from "../types";

interface MapPageProps {
    queryResult: CountryInfo[] | null;
    targetDiv: RefObject<HTMLDivElement>;
}

const MapePage: React.FC<MapPageProps> = ({queryResult, targetDiv}) => {


    return <div className="map-page-container" ref={targetDiv}><Map queryResult={queryResult}></Map></div>;
}

export default MapePage;