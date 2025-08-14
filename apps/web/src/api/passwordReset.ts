import { api } from "../api";

export const requestReset = async (email: string) => {
  await api.post("/auth/forgot", { email });
};

export const resetPassword = async (token: string, password: string) => {
  await api.post("/auth/reset", { token, password });
};
