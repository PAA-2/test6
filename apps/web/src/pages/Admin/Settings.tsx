import { useEffect, useState } from "react";
import { AppSetting, listSettings, updateSetting } from "../../api/admin";

export default function SettingsPage() {
  const [settings, setSettings] = useState<AppSetting[]>([]);
  useEffect(() => {
    listSettings().then(setSettings);
  }, []);
  const save = async (key: string, value: any) => {
    await updateSetting(key, value);
  };
  return (
    <div>
      <h1>Settings</h1>
      <ul>
        {settings.map((s) => (
          <li key={s.key}>
            {s.key}
            <input
              value={JSON.stringify(s.value)}
              onChange={(e) =>
                setSettings((all) =>
                  all.map((x) =>
                    x.key === s.key ? { ...x, value: e.target.value } : x,
                  ),
                )
              }
            />
            <button onClick={() => save(s.key, s.value)}>Save</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
