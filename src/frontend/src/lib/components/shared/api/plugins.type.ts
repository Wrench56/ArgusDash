export type PluginStatusContainer = {
  ok: boolean;
  plugins: Array<PluginStatus>;
};

export type PluginStatus = {
  name: string;
  status: boolean;
};
