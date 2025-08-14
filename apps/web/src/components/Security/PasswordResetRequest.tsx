import { useState } from "react";
import { requestReset } from "../../api/passwordReset";

export default function PasswordResetRequest() {
  const [email, setEmail] = useState("");
  const [sent, setSent] = useState(false);
  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    await requestReset(email);
    setSent(true);
  };
  if (sent) return <p>Check your email.</p>;
  return (
    <form onSubmit={submit}>
      <input
        aria-label="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <button type="submit">Send reset</button>
    </form>
  );
}
