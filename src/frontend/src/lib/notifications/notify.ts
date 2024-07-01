import { writable, type Writable } from "svelte/store";
import NotificationStore from "./store";

export enum NotificationPriority {
  Default = "default",
  Info = "info",
  System = "system",
}

export enum NotificationState {
  Appear = "appear",
  Alive = "alive",
  Disappear = "disappear",
  Dead = "dead",
}

type NotificationInterface = {
  title: string;
} & NotificationOptions;

export type DNotificationOptions = {
  priority: NotificationPriority;
  duration: number;
  state: Writable<NotificationState>;
  after: CallableFunction;
};

export type NotificationWrapper = {
  data: DNotificationOptions;
  notification: NotificationInterface;
};

type NotifyOptions = {
  title: string;
  options: NotificationOptions;
  priority: NotificationPriority;
  notifyDesktop?: boolean;
  duration?: number;
};

export function notify(nOptions: NotifyOptions) {
  NotificationStore.update((array: NotificationWrapper[]) => {
    let data = {
      priority: nOptions.priority || NotificationPriority.Default,
      duration: nOptions.duration,
      state: writable(NotificationState.Appear),
      after: () => {},
    };

    nOptions.options.data ??= {};
    nOptions.options.data.id = uniqueId();

    if (nOptions.notifyDesktop) {
      const NOTIFICATION = new Notification(nOptions.title, nOptions.options);
      data.after = () => NOTIFICATION.close();

      return [
        ...array,
        {
          data: data,
          notification: NOTIFICATION,
        },
      ];
    }

    return [
      ...array,
      {
        data: data,
        notification: {
          title: nOptions.title,
          ...nOptions.options,
        },
      },
    ];
  });
}

function uniqueId(): number {
  return parseInt(
    Math.ceil(Math.random() * Date.now())
      .toPrecision(16)
      .toString()
      .replace(".", "")
  );
}
