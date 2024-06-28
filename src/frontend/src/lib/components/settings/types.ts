type SettingsApi = {
  update(new_status: string): void;
  keyPressed(event: KeyboardEvent): boolean;
  setCursor(enable: boolean): void;
};
