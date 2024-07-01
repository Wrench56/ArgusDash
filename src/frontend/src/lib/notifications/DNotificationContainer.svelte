<script lang="ts">
  import { get } from "svelte/store";
  import DNotification from "./DNotification.svelte";
  import { NotificationState, type NotificationWrapper } from "./notify";
  import NotificationStore from "./store";

  let notification: NotificationWrapper;
  let notification_state: NotificationState = NotificationState.Dead;

  NotificationStore.subscribe(fetchNextNotification);
  export function fetchNextNotification(array: NotificationWrapper[]) {
    if (array.length == 0) {
      return;
    }

    if (notification_state == NotificationState.Dead) {
      notification = array.shift();
      notification_state = get(notification.data.state);
      notification.data.state.subscribe((state) => {
        if (state == NotificationState.Dead) {
          notification_state = get(notification.data.state);
          fetchNextNotification(get(NotificationStore));
        }
      });
      console.log(notification.notification.data.id);
    }
  }
</script>

<div class="container">
  {#if notification && get(notification.data.state) != NotificationState.Dead}
    <DNotification wrapper={notification} />
  {/if}
</div>

<style>
  .container {
    position: fixed;
    right: 0px;
    top: 0px;
    width: 269px;
    height: 135px;
    text-align: center;
    overflow: scroll;
    background-color: transparent;
  }

  .container::-webkit-scrollbar {
    width: 1px;
  }

  .container::-webkit-scrollbar-thumb {
    background-color: transparent;
    outline: 1px solid rgb(0, 128, 255);
  }

  .container::-webkit-scrollbar-corner {
    background: transparent;
  }
</style>
