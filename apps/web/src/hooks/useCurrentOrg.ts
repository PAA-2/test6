import { useEffect, useState } from 'react';
import { listOrgs, setCurrentOrg, Organization } from '../api/orgs';

export function useCurrentOrg() {
  const [orgs, setOrgs] = useState<Organization[]>([]);
  const [current, setCurrent] = useState<string | undefined>(undefined);

  useEffect(() => {
    listOrgs().then((o) => {
      setOrgs(o);
      if (!current && o.length > 0) setCurrent(o[0].id);
    });
  }, []);

  const change = async (id: string) => {
    setCurrent(id);
    await setCurrentOrg(id);
  };

  return { orgs, current, change };
}
