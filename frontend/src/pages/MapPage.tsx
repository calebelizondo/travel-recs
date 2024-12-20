import { RefObject } from "react";
import Map from "../components/Map";
import { CountryInfo } from "../types";

interface MapPageProps {
    queryResult: CountryInfo[] | null;
    targetDiv: RefObject<HTMLDivElement>;
    isLoading: boolean;
}

const MapePage: React.FC<MapPageProps> = ({ queryResult, targetDiv, isLoading }) => {

    if ((queryResult === null || queryResult.length === 0) && isLoading === false) return <></>;

    return (
        <div className="map-page-container" ref={targetDiv}>
            {isLoading ? (
                <div className="loading-indicator">
                    <div className="spinner"></div>
                </div>
            ) : (
                <>
                    <br />
                    <br />
                    <Map queryResult={queryResult} />
                </>
            )}
        </div>
    );
};

export default MapePage;
