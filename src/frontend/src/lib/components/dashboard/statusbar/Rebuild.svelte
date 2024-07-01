<script lang="ts">
  import { NotificationPriority, notify } from "$lib/notifications/notify";
  import { onMount } from "svelte";

  onMount(() => {
    if (localStorage.getItem("rebuild") != null) {
      notify({
        title: "Site rebuilt",
        priority: NotificationPriority.System,
        duration: 2000,
        options: {
          body: localStorage.getItem("rebuild"),
        },
        notifyDesktop: false,
      });
    }
  });

  function rebuild() {
    fetch("/rebuild", { method: "POST" }).then((response) => {
      if (response.ok) {
        response.text().then((text) => {
          if (text.startsWith("REBUILT")) {
            localStorage.setItem("rebuild", text.substring(9));
            location.reload();
          }
        });
      }
    });
  }
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div on:click={() => rebuild()}>Rebuild</div>

<style>
  div {
    height: 100%;
    padding-top: 8px;
    text-align: center;
    color: whitesmoke;
    font-family: monaco, Consolas, "Lucida Console", monospace;
    font-size: 12px;
    margin: 0px;
    display: grid;
    grid-column: 2;
  }

  div:hover {
    background-color: rgb(102, 153, 255);
    cursor: pointer;
  }
</style>
