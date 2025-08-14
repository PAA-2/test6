import { useState } from 'react';

export default function CopyOnceSecret({ secret }: { secret: string }) {
  const [shown, setShown] = useState(true);
  return (
    <div>
      {shown ? (
        <div>
          <code>{secret}</code>
          <button
            onClick={() => {
              navigator.clipboard.writeText(secret);
              setShown(false);
            }}
          >
            Copy
          </button>
        </div>
      ) : (
        <span>secret copied</span>
      )}
    </div>
  );
}
