import { useState } from 'react';
import { useCurrentOrg } from '../hooks/useCurrentOrg';

export default function OrgSettings() {
  const { current } = useCurrentOrg();
  const [name, setName] = useState('');
  const save = () => {
    // placeholder, no API implemented
    console.log('save', current, name);
  };
  return (
    <div>
      <input aria-label="name" value={name} onChange={(e) => setName(e.target.value)} />
      <button onClick={save}>Save</button>
    </div>
  );
}
