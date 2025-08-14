import { SearchItem } from '../api/search';

interface Props {
  items?: SearchItem[];
}

export default function SearchResults({ items = [] }: Props) {
  return (
    <ul>
      {items.map((i) => (
        <li key={i.id}>
          <strong>{i.title}</strong>
          <div dangerouslySetInnerHTML={{ __html: i.snippet }} />
        </li>
      ))}
    </ul>
  );
}
