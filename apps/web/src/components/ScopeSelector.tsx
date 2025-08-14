interface Props {
  selected: string[];
  onChange: (scopes: string[]) => void;
}

const ALL_SCOPES = ['projects:read', 'projects:write', 'files:read'];

export default function ScopeSelector({ selected, onChange }: Props) {
  function toggle(scope: string) {
    if (selected.includes(scope)) {
      onChange(selected.filter((s) => s !== scope));
    } else {
      onChange([...selected, scope]);
    }
  }
  return (
    <div>
      {ALL_SCOPES.map((s) => (
        <label key={s}>
          <input
            type="checkbox"
            checked={selected.includes(s)}
            onChange={() => toggle(s)}
          />
          {s}
        </label>
      ))}
    </div>
  );
}
