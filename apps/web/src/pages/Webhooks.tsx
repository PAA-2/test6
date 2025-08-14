import { useEffect, useState } from 'react';
import { createWebhook, listWebhooks, sendTest, WebhookEndpoint } from '../api/devPortal';
import { useCurrentOrg } from '../hooks/useCurrentOrg';

export default function Webhooks() {
  const { current } = useCurrentOrg();
  const [hooks, setHooks] = useState<WebhookEndpoint[]>([]);
  const [url, setUrl] = useState('');
  const [events, setEvents] = useState<string>('project.created');
  const [secret, setSecret] = useState<string | null>(null);

  useEffect(() => {
    if (current) listWebhooks(current).then(setHooks);
  }, [current]);

  async function handleCreate() {
    if (!current) return;
    const res = await createWebhook(current, url, [events]);
    setSecret(res.secret);
    listWebhooks(current).then(setHooks);
  }

  return (
    <div>
      <h2>Webhooks</h2>
      <div>
        <input value={url} onChange={(e) => setUrl(e.target.value)} placeholder="URL" />
        <select value={events} onChange={(e) => setEvents(e.target.value)}>
          <option value="project.created">project.created</option>
          <option value="project.updated">project.updated</option>
          <option value="file.uploaded">file.uploaded</option>
        </select>
        <button onClick={handleCreate}>Create</button>
      </div>
      {secret && <div>secret: <code>{secret}</code></div>}
      <ul>
        {hooks.map((h) => (
          <li key={h.id}>
            {h.url} [{h.events.join(', ')}]
            {current && <button onClick={() => sendTest(current, h.id)}>Send test</button>}
          </li>
        ))}
      </ul>
    </div>
  );
}
