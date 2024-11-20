import './styles.css';
import SearchBar from '../components/SearchBar';
import { CountryInfo } from '../types';

interface LandingPageProps {
    setQueryResult: (result: CountryInfo[] | null) => void;
}

const LandingPage: React.FC<LandingPageProps> = ({setQueryResult}) => {
    return <div className="landing-page-container">
        <div className="landing-page-content">
            <p>Where to?</p>
            <SearchBar setQueryResult={setQueryResult}></SearchBar>
        </div>

    </div>
}

export default LandingPage;