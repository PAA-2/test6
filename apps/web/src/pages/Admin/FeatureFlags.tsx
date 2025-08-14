import { useEffect, useState } from "react";
import { FeatureFlag, listFlags, updateFlag } from "../../api/admin";

export default function FeatureFlagsPage() {
  const [flags, setFlags] = useState<FeatureFlag[]>([]);
  useEffect(() => {
    listFlags().then(setFlags);
  }, []);
  const toggle = async (key: string, enabled: boolean) => {
    await updateFlag(key, !enabled);
    setFlags((f) => f.map((x) => (x.key === key ? { ...x, enabled: !enabled } : x)));
  };
  return (
    <div>
      <h1>Feature Flags</h1>
      <ul>
        {flags.map((f) => (
          <li key={f.key}>
            {f.key}
            <input
              type="checkbox"
              checked={f.enabled}
              onChange={() => toggle(f.key, f.enabled)}
            />
          </li>
        ))}
      </ul>
    </div>
  );
}
