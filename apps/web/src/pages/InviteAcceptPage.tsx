import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getInvite, acceptInvite } from '../api/orgs';

export default function InviteAcceptPage() {
  const { token } = useParams<{ token: string }>();
  const [valid, setValid] = useState(false);
  useEffect(() => {
    if (token) {
      getInvite(token)
        .then(() => setValid(true))
        .catch(() => setValid(false));
    }
  }, [token]);
  if (!token) return <div>Invalid</div>;
  if (!valid) return <div>Invalid</div>;
  return <button onClick={() => token && acceptInvite(token)}>Join</button>;
}
