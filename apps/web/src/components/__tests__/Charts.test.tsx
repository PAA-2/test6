import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom/vitest';
import LineChart from '../LineChart';
import BarChart from '../BarChart';

describe('Charts', () => {
  it('renders line chart', () => {
    render(<LineChart data={[{ date: '2024-01-01', count: 1 }]} />);
    expect(screen.getByRole('img', { name: /line-chart/i })).toBeInTheDocument();
  });
  it('renders bar chart', () => {
    render(<BarChart data={[{ label: 'pdf', value: 2 }]} />);
    expect(screen.getByLabelText('pdf')).toBeInTheDocument();
  });
});
