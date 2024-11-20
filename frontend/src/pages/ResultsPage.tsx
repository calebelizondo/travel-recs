import { CountryInfo } from "../types"

interface ResultsPageProps {
    queryResults: CountryInfo[] | null;
};

const ResultsPage: React.FC<ResultsPageProps> = ({queryResults}) => {
    if (queryResults === null) return <></>;


    return <></>;
};

export default ResultsPage;