import { InputAdornment, TextField } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';

interface SearchBarProps {}

const SearchBar: React.FC<SearchBarProps> = () => {
  return (
    <TextField
      variant="outlined"
      fullWidth
      margin="normal"
      InputProps={{
        startAdornment: (
          <InputAdornment position="start">
            <SearchIcon />
          </InputAdornment>
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
}

export default SearchBar;
