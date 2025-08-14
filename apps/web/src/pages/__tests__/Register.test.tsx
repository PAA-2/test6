import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom/vitest';
import Register from '../Register';

describe('Register', () => {
  it('renders form', () => {
    render(<Register />);
    expect(screen.getByPlaceholderText(/email/i)).toBeInTheDocument();
  });
});
