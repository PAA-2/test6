export default function DeliveryStatusBadge({ status }: { status: string }) {
  const color = status === 'sent' ? 'green' : status === 'failed' ? 'red' : 'gray';
  return <span style={{ color }}>{status}</span>;
}
