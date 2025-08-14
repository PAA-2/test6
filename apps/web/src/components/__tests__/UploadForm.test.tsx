import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom/vitest';
import UploadForm from '../UploadForm';

vi.stubGlobal('fetch', vi.fn(() => Promise.resolve({ ok: true, json: () => Promise.resolve({}) })));

describe('UploadForm', () => {
  it('uploads file and shows progress', async () => {
    const onUploaded = vi.fn();
    render(<UploadForm token="t" onUploaded={onUploaded} />);
    const fileInput = screen.getByTestId('file-input') as HTMLInputElement;
    const file = new File(['hello'], 'test.pdf', { type: 'application/pdf' });
    fireEvent.change(fileInput, { target: { files: [file] } });
    fireEvent.submit(screen.getByTestId('upload-form'));
    await waitFor(() => expect(onUploaded).toHaveBeenCalled());
    expect(screen.getByTestId('progress')).toHaveAttribute('value', '100');
  });
});
