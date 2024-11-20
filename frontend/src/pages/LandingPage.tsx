import './styles.css';
import SearchBar from '../components/SearchBar';
import { CountryInfo } from '../types';

interface LandingPageProps {
    setQueryResult: (result: CountryInfo[] | null) => void;
    setIsLoading: (isLoading: boolean) => void;
}

const LandingPage: React.FC<LandingPageProps> = ({setQueryResult, setIsLoading}) => {
    return <div className="landing-page-container">
        <div className="landing-page-content">
            <p>Where to?</p>
            <SearchBar setQueryResult={setQueryResult} setIsLoading={setIsLoading}></SearchBar>
        </div>

    </div>
}

export default LandingPage;