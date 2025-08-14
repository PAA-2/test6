import { FacetsResponse } from '../api/search';

interface Props {
  facets: FacetsResponse | null;
}

export default function FacetPanel({ facets }: Props) {
  if (!facets) return null;
  return (
    <div>
      <div>
        <h4>Project status</h4>
        <ul>
          {Object.entries(facets.projects_by_status).map(([k, v]) => (
            <li key={k}>
              {k}: {v}
            </li>
          ))}
        </ul>
      </div>
      <div>
        <h4>File types</h4>
        <ul>
          {facets.files_by_mime.map((m) => (
            <li key={m.mime}>
              {m.mime}: {m.count}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
