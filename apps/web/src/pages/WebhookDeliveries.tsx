import { useEffect, useState } from 'react';
import { listDeliveries, Delivery } from '../api/devPortal';
import { useCurrentOrg } from '../hooks/useCurrentOrg';
import DeliveryStatusBadge from '../components/DeliveryStatusBadge';

export default function WebhookDeliveries({ endpointId }: { endpointId: string }) {
  const { current } = useCurrentOrg();
  const [deliveries, setDeliveries] = useState<Delivery[]>([]);
  useEffect(() => {
    if (current) listDeliveries(current, endpointId).then(setDeliveries);
  }, [current, endpointId]);
  return (
    <div>
      <h3>Deliveries</h3>
      <ul>
        {deliveries.map((d) => (
          <li key={d.id}>
            {d.event} - <DeliveryStatusBadge status={d.status} /> ({d.response_code})
          </li>
        ))}
      </ul>
    </div>
  );
}
