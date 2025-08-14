import { api } from "../api";

export type FeatureFlag = { key: string; enabled: boolean };

export const listFlags = async (): Promise<FeatureFlag[]> => {
  const res = await api.get<FeatureFlag[]>("/feature-flags");
  return res.data;
};

export const updateFlag = async (key: string, enabled: boolean) => {
  const res = await api.patch<FeatureFlag>(`/feature-flags/${key}`, { enabled });
  return res.data;
};

export type AppSetting = { key: string; value: any };

export const listSettings = async (): Promise<AppSetting[]> => {
  const res = await api.get<AppSetting[]>("/app-settings");
  return res.data;
};

export const updateSetting = async (key: string, value: any) => {
  const res = await api.patch<AppSetting>(`/app-settings/${key}`, { value });
  return res.data;
};
