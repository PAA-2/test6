import { SavedSearch } from '../api/search';

interface Props {
  searches: SavedSearch[];
  onRun: (params: Record<string, any>) => void;
  onDelete: (id: string) => void;
}

export default function SavedSearchesPanel({ searches, onRun, onDelete }: Props) {
  return (
    <ul>
      {searches.map((s) => (
        <li key={s.id}>
          <button onClick={() => onRun(s.params)}>{s.name}</button>
          <button onClick={() => onDelete(s.id)}>x</button>
        </li>
      ))}
    </ul>
  );
}
