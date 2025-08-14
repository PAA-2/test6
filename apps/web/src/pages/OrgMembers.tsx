import { useEffect, useState } from 'react';
import { listMembers } from '../api/orgs';
import { useCurrentOrg } from '../hooks/useCurrentOrg';

export default function OrgMembers() {
  const { current } = useCurrentOrg();
  const [members, setMembers] = useState<{ user_id: number; role: string }[]>([]);
  useEffect(() => {
    if (current) listMembers(current).then(setMembers);
  }, [current]);
  return (
    <ul>
      {members.map((m) => (
        <li key={m.user_id}>{m.user_id}: {m.role}</li>
      ))}
    </ul>
  );
}
