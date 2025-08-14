import { useState } from 'react';
import { createInvite } from '../api/orgs';
import { useCurrentOrg } from '../hooks/useCurrentOrg';

export default function OrgInvites() {
  const { current } = useCurrentOrg();
  const [email, setEmail] = useState('');
  const [token, setToken] = useState('');
  const submit = async () => {
    if (current) {
      const res = await createInvite(current, email, 'member');
      setToken(res.token);
    }
  };
  return (
    <div>
      <input aria-label="email" value={email} onChange={(e) => setEmail(e.target.value)} />
      <button onClick={submit}>Invite</button>
      {token && <span>{token}</span>}
    </div>
  );
}
