<script lang="ts">
  import Statusbar from "$lib/components/shared/statusbar/Statusbar.svelte";
  import DNotificationContainer from "$lib/notifications/DNotificationContainer.svelte";
</script>

<Statusbar />
<DNotificationContainer />

<style>
  :root {
    background-color: black;
  }
</style>
