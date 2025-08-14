import { useState } from 'react';
import { uploadFile, FileMeta } from '../api/files';

interface Props {
  token: string;
  onUploaded: (f: FileMeta) => void;
}

export default function UploadForm({ token, onUploaded }: Props) {
  const [progress, setProgress] = useState(0);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const input = e.currentTarget.elements.namedItem('file') as HTMLInputElement;
    if (!input.files || input.files.length === 0) return;
    setProgress(0);
    const file = input.files[0];
    const uploaded = await uploadFile(token, file);
    setProgress(100);
    onUploaded(uploaded);
    input.value = '';
  };

  return (
    <form onSubmit={handleSubmit} data-testid="upload-form">
      <input type="file" name="file" data-testid="file-input" />
      <button type="submit">Upload</button>
      {progress > 0 && (
        <progress value={progress} max="100" data-testid="progress" />
      )}
    </form>
  );
}
