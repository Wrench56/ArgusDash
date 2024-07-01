import { writable } from "svelte/store";
import type { NotificationWrapper } from "./notify";

const NotificationStore = writable<NotificationWrapper[]>([]);

export default NotificationStore;
