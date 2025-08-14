import { render, screen } from "@testing-library/react";
import { test, expect, vi } from "vitest";
vi.mock("../../api/admin", () => ({ listFlags: () => Promise.resolve([]), updateFlag: vi.fn() }));
import FeatureFlagsPage from "../Admin/FeatureFlags";

test("renders list", () => {
  render(<FeatureFlagsPage />);
  expect(screen.getByText(/Feature Flags/)).toBeTruthy();
});
