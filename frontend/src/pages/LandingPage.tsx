import './styles.css';
import SearchBar from '../components/SearchBar';

interface LandingPageProps {

}

const LandingPage: React.FC<LandingPageProps> = () => {
    return <div className="landing-page-container">
        <div>
            <p>Where to?</p>
            <SearchBar></SearchBar>
        </div>

    </div>
}

export default LandingPage;