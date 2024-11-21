import { CountryInfo, Climate, Cost } from "../types"

interface ResultsPageProps {
    queryResult: CountryInfo[] | null;
};

const ResultsPage: React.FC<ResultsPageProps> = ({queryResult}) => {
    if ((queryResult === null || queryResult.length === 0)) return <></>;

    const climateIcons: { [key in Climate]: string } = {
        hot: "🌞",
        cold: "❄️",
        humid: "💧",
    };

    const costSymbols: { [key in Cost]: string } = {
        1: "$",
        2: "$$",
        3: "$$$",
    };
    
  return (
    <div className="results-container">
      {queryResult.map((country) => (
        <div className="country-card" key={country.code}>
          <h2 className="country-name">{country.name.toUpperCase()}</h2>
          <p className="country-bio">{country.info.bio}</p>
          <div className="country-climate">
            {country.info.climate.map((climate) => (
              <span key={climate} className="climate-icon">
                {climateIcons[climate]}
              </span>
            ))}
          </div>
          <div className="country-cost">{costSymbols[country.info.cost]}</div>
        </div>
      ))}
    </div>
  );
};

export default ResultsPage;