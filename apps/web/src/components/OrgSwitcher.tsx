import { useCurrentOrg } from '../hooks/useCurrentOrg';

export default function OrgSwitcher() {
  const { orgs, current, change } = useCurrentOrg();
  if (orgs.length === 0) return null;
  return (
    <select aria-label="organization" value={current} onChange={(e) => change(e.target.value)}>
      {orgs.map((o) => (
        <option key={o.id} value={o.id}>
          {o.name}
        </option>
      ))}
    </select>
  );
}
