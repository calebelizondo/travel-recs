import './styles.css';
import SearchBar from '../components/SearchBar';
import { CountryInfo } from '../types';

interface LandingPageProps {
    setQueryResult: (result: CountryInfo[] | null) => void;
    setIsLoading: (isLoading: boolean) => void;
    query: string;
    setQuery: (q: string) => void;
}

const LandingPage: React.FC<LandingPageProps> = ({setQueryResult, setIsLoading, query, setQuery}) => {
    return <div className="landing-page-container">
        <div className="landing-page-content">
            <p>Where to?</p>
            <SearchBar setQueryResult={setQueryResult} setIsLoading={setIsLoading} query={query} setQuery={setQuery}></SearchBar>
        </div>

    </div>
}

export default LandingPage;