import { CountryInfo, Filter } from "../types";
import SearchBar from "./SearchBar";


interface BarProps {
    setQueryResult: (result: CountryInfo[] | null) => void;
    setIsLoading: (isLoading: boolean) => void;
    query: string;
    setQuery: (q: string) => void;
    filter: Filter;
    setFilter: (f: Filter) => void;
}

const Bar: React.FC<BarProps> = ({setQueryResult, setIsLoading, query, setQuery, filter, setFilter}) => {

    return (<>
    <div className="sticky-bar-container">
        <SearchBar setQueryResult={setQueryResult} setIsLoading={setIsLoading} query={query} setQuery={setQuery}></SearchBar>
    </div>
    </>);
}

export default Bar;