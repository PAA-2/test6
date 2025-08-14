interface Props {
  data: { label: string; value: number }[];
}

export default function BarChart({ data }: Props) {
  const max = Math.max(...data.map((d) => d.value), 1);
  return (
    <div>
      {data.map((d) => (
        <div key={d.label} style={{ display: 'flex', alignItems: 'center' }}>
          <span style={{ width: '80px' }}>{d.label}</span>
          <div
            aria-label={d.label}
            style={{
              height: '10px',
              background: 'green',
              width: `${(d.value / max) * 100}%`,
              marginLeft: '4px',
            }}
          />
        </div>
      ))}
    </div>
  );
}
