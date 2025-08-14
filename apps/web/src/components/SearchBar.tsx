import { useState } from 'react';

interface Props {
  onSearch: (q: string) => void;
  initial?: string;
}

export default function SearchBar({ onSearch, initial = '' }: Props) {
  const [value, setValue] = useState(initial);
  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        onSearch(value);
      }}
    >
      <input aria-label="search" value={value} onChange={(e) => setValue(e.target.value)} />
      <button type="submit">Search</button>
    </form>
  );
}
