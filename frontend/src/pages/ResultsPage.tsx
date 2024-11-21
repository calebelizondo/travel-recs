import { CountryInfo, Climate, Cost, cutoff, climateIcons, costSymbols } from "../types"

interface ResultsPageProps {
    queryResult: CountryInfo[] | null;
};

const img_urls = ["https://www.introtravel.com/media/images/-kZM4gOw.width-800.jpg", 
    "https://www.atlasandboots.com/wp-content/uploads/2019/05/ama-dablam2-most-beautiful-mountains-in-the-world.jpg",
    "https://aebc975c.rocketcdn.me/wp-content/uploads/2020/12/plage.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/View_of_Empire_State_Building_from_Rockefeller_Center_New_York_City_dllu_%28cropped%29.jpg/640px-View_of_Empire_State_Building_from_Rockefeller_Center_New_York_City_dllu_%28cropped%29.jpg", 
    "https://media.cntraveler.com/photos/63482b255e7943ad4006df0b/16:9/w_1280,c_limit/tokyoGettyImages-1031467664.jpeg", 
    "https://cdn.mos.cms.futurecdn.net/3FnczamRyWU6MvRMEXWaGD.jpg"]

const ResultsPage: React.FC<ResultsPageProps> = ({queryResult}) => {
    if ((queryResult === null || queryResult.length === 0)) return <></>;

    const results = queryResult.slice(0, cutoff);
    
    return (
        <div className="results-container">
        {results.map((country) => (
            <div className="country-card" key={country.code} id={`country-${country.code}`}>
            <div className="country-header">
                <h2 className="country-name">{country.name.toUpperCase()}</h2>
                    <div className="country-climate">
                    {country.info.climate.map((climate) => (
                    <span key={climate} className="climate-icon">
                        {climateIcons[climate]}
                    </span>
                    ))}
                </div>
                <div className="country-cost">{costSymbols[country.info.cost]}</div>
            </div>
            <br />
            <div className="country-content">
                <img src={img_urls[Math.floor(Math.random() * img_urls.length)]} alt="travel" />
                <p className="country-bio">{country.info.bio}</p>
            </div>
            </div>
        ))}
        </div>
    );
};

export default ResultsPage;