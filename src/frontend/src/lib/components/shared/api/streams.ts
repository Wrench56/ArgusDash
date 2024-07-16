type CallbackFunction = (data: any) => void;
let pluginStatusStream = undefined;

const createEventSource = (
  url: string,
  defaultData: object
): {
  subscribe: (listener: CallbackFunction) => () => boolean;
  fetch: () => object;
  close: () => void;
} => {
  const eventSource = new EventSource(url);
  const listeners: Set<CallbackFunction> = new Set();
  let cachedData: object = defaultData;

  eventSource.onmessage = (event: MessageEvent) => {
    cachedData = JSON.parse(event.data);
    listeners.forEach((listener) => listener(cachedData));
  };

  eventSource.onerror = () => {
    const errorData = defaultData;
    listeners.forEach((listener) => listener(errorData));
  };

  return {
    subscribe: (listener) => {
      listeners.add(listener);
      return () => listeners.delete(listener);
    },
    close: () => {
      eventSource.close();
    },
    fetch: () => {
      return cachedData;
    },
  };
};

export function initEventSources() {
  if (pluginStatusStream == undefined) {
    pluginStatusStream = createEventSource("/plugins/status", {
      ok: false,
      plugins: [],
    });
  }
}

export { pluginStatusStream };
