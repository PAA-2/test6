import { useEffect, useState } from 'react';
import { createApiKey, listApiKeys, ApiKey } from '../api/devPortal';
import CopyOnceSecret from '../components/CopyOnceSecret';
import ScopeSelector from '../components/ScopeSelector';
import { useCurrentOrg } from '../hooks/useCurrentOrg';

export default function ApiKeys() {
  const { current } = useCurrentOrg();
  const [keys, setKeys] = useState<ApiKey[]>([]);
  const [name, setName] = useState('');
  const [scopes, setScopes] = useState<string[]>([]);
  const [newKey, setNewKey] = useState<string | null>(null);

  useEffect(() => {
    if (current) {
      listApiKeys(current).then(setKeys);
    }
  }, [current]);

  async function handleCreate() {
    if (!current) return;
    const res = await createApiKey(current, name, scopes);
    setNewKey(res.key);
    listApiKeys(current).then(setKeys);
  }

  return (
    <div>
      <h2>API Keys</h2>
      <div>
        <input value={name} onChange={(e) => setName(e.target.value)} placeholder="name" />
        <ScopeSelector selected={scopes} onChange={setScopes} />
        <button onClick={handleCreate}>Create</button>
      </div>
      {newKey && <CopyOnceSecret secret={newKey} />}
      <ul>
        {keys.map((k) => (
          <li key={k.id}>
            {k.name} ({k.prefix}) - {k.scopes.join(', ')}
          </li>
        ))}
      </ul>
    </div>
  );
}
