let isSelectorVisible: boolean = $state(false);

export function showWidgetSelector() {
  isSelectorVisible = true;
}

export function hideWidgetSelector() {
  isSelectorVisible = false;
}

export function getSelectorVisibleRune() {
  return isSelectorVisible;
}
