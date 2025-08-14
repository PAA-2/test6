interface Props {
  status: string;
}

export default function JobStatusBadge({ status }: Props) {
  const color =
    status === 'finished'
      ? 'green'
      : status === 'failed'
      ? 'red'
      : 'gray';
  return <span style={{ color }}>{status}</span>;
}
