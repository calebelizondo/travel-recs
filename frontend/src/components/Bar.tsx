import { CountryInfo } from "../types";
import SearchBar from "./SearchBar";


interface BarProps {
    setQueryResult: (result: CountryInfo[] | null) => void;
    setIsLoading: (isLoading: boolean) => void;
}

const Bar: React.FC<BarProps> = ({setQueryResult, setIsLoading}) => {

    return (<>
    <div className="sticky-bar-container">
        <SearchBar setQueryResult={setQueryResult} setIsLoading={setIsLoading}></SearchBar>
    </div>
    </>);
}

export default Bar;