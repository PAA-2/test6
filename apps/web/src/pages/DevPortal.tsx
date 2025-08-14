import { Link } from 'react-router-dom';

export default function DevPortal() {
  return (
    <div>
      <h1>Developer Portal</h1>
      <ul>
        <li>
          <Link to="/dev/api-keys">API Keys</Link>
        </li>
        <li>
          <Link to="/dev/webhooks">Webhooks</Link>
        </li>
      </ul>
    </div>
  );
}
