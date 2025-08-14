interface Props {
  data: { date: string; count: number }[];
}

export default function LineChart({ data }: Props) {
  const max = Math.max(...data.map((d) => d.count), 1);
  const points = data
    .map((d, i) => {
      const x = (i / Math.max(data.length - 1, 1)) * 100;
      const y = 100 - (d.count / max) * 100;
      return `${x},${y}`;
    })
    .join(' ');
  return (
    <svg role="img" aria-label="line-chart" viewBox="0 0 100 100">
      <polyline
        fill="none"
        stroke="blue"
        strokeWidth="1"
        points={points}
      />
    </svg>
  );
}
