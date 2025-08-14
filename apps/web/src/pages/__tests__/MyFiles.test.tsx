import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom/vitest';
import MyFiles from '../MyFiles';

vi.mock('../../hooks/useFiles', () => ({
  useFiles: () => ({
    data: [
      {
        id: '1',
        original_name: 'a.png',
        mime_type: 'image/png',
        size_bytes: 1,
        created_at: new Date().toISOString(),
      },
    ],
    loading: false,
    error: null,
  }),
}));

vi.mock('../../api/files', () => ({
  deleteFileApi: vi.fn(),
  downloadFile: vi.fn().mockResolvedValue(new Blob()),
}));

vi.mock('../../api/jobs', () => ({
  enqueueThumbnail: vi.fn().mockResolvedValue({ task_id: 'j1' }),
}));

vi.mock('../../hooks/useJobStatus', () => ({
  useJobStatus: () => ({ status: 'finished' }),
}));

vi.mock('../../components/UploadForm', () => ({
  default: () => <div>UploadForm</div>,
}));

describe('MyFiles', () => {
  it('allows thumbnail regeneration', async () => {
    render(<MyFiles token="t" />);
    const btn = screen.getByText('Thumbnail');
    await userEvent.click(btn);
    expect(await screen.findByText('finished')).toBeInTheDocument();
  });
});
