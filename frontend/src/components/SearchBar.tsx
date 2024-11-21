import React, { useState } from 'react';
import { InputAdornment, TextField, IconButton } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import { CountryInfo } from '../types';

interface SearchBarProps {
  setQueryResult: (result: CountryInfo[] | null) => void;
  setIsLoading: (isLoading: boolean) => void;
  query: string;
  setQuery: (q: string) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ setQueryResult, setIsLoading, query, setQuery }) => {

  const baseUrl =
    process.env.NODE_ENV === 'production'
      ? 'https://travel-recs-backend.onrender.com/'
      : 'http://localhost:8000';

  const handleSearch = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(`${baseUrl}/query/?query=${encodeURIComponent(query)}`);
      if (response.ok) {
        const result: {results: CountryInfo[]} = await response.json();
        setQueryResult(result.results);
      } else {
        console.error('Failed to fetch query results:', response.statusText);
        setQueryResult(null);
      }
    } catch (error) {
      console.error('Error while fetching query results:', error);
      setQueryResult(null);
    }
  };

  const handleKeyDown = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <TextField
      value={query}
      onChange={(e) => setQuery(e.target.value)}
      onKeyDown={handleKeyDown}
      variant="outlined"
      fullWidth
      margin="normal"
      placeholder="Try 'spicy food and nice ocean views'"
      InputProps={{
        endAdornment: (
          
            <IconButton onClick={handleSearch}>
              <SearchIcon />
            </IconButton>
       
        ),
      }}
      sx={{
        backgroundColor: 'white',
        borderRadius: '25px',
        '& .MuiOutlinedInput-root': {
          borderRadius: '25px',
        },
        '& .MuiInputLabel-root': {
          marginLeft: '10px',
        },
        '& .MuiOutlinedInput-notchedOutline': {
          borderColor: '#ccc',
        },
        '&:hover .MuiOutlinedInput-notchedOutline': {
          borderColor: '#aaa',
        },
      }}
    />
  );
};

export default SearchBar;
