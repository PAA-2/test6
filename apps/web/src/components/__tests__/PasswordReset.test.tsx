import { render, screen } from "@testing-library/react";
import { test, expect } from "vitest";
import PasswordResetRequest from "../Security/PasswordResetRequest";

test("renders email input", () => {
  render(<PasswordResetRequest />);
  expect(screen.getByLabelText(/email/i)).toBeTruthy();
});
