import { useState } from "react";
import { resetPassword } from "../../api/passwordReset";

export default function PasswordResetForm() {
  const [token, setToken] = useState("");
  const [password, setPassword] = useState("");
  const [done, setDone] = useState(false);
  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    await resetPassword(token, password);
    setDone(true);
  };
  if (done) return <p>Password changed.</p>;
  return (
    <form onSubmit={submit}>
      <input
        aria-label="token"
        value={token}
        onChange={(e) => setToken(e.target.value)}
      />
      <input
        aria-label="password"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button type="submit">Reset</button>
    </form>
  );
}
