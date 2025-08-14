import { useState } from 'react';
import UploadForm from '../components/UploadForm';
import { useFiles } from '../hooks/useFiles';
import { deleteFileApi, downloadFile, FileMeta } from '../api/files';

interface Props {
  token: string;
}

export default function MyFiles({ token }: Props) {
  const [reload, setReload] = useState(0);
  const { data, loading, error } = useFiles(token, reload);

  const handleUploaded = () => setReload((r) => r + 1);

  const handleDelete = async (id: string) => {
    if (!confirm('Delete file?')) return;
    await deleteFileApi(token, id);
    setReload((r) => r + 1);
  };

  const handleDownload = async (id: string, name: string) => {
    const blob = await downloadFile(token, id);
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = name;
    a.click();
    window.URL.revokeObjectURL(url);
  };

  return (
    <div>
      <h1>My Files</h1>
      <UploadForm token={token} onUploaded={handleUploaded} />
      {loading && <p>Loading...</p>}
      {error && <p>{error}</p>}
      {!loading && data.length === 0 && <p>No files</p>}
      {data.length > 0 && (
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Size</th>
              <th>Date</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {data.map((f: FileMeta) => (
              <tr key={f.id}>
                <td>{f.original_name}</td>
                <td>{f.size_bytes}</td>
                <td>{new Date(f.created_at).toLocaleString()}</td>
                <td>
                  <button onClick={() => handleDownload(f.id, f.original_name)}>
                    Download
                  </button>
                  <button onClick={() => handleDelete(f.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
