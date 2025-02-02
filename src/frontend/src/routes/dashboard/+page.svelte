<script lang="ts">
  import WidgetSelector from "$lib/components/dashboard/WidgetSelector.svelte";
  import Statusbar from "$lib/components/shared/statusbar/Statusbar.svelte";
  import DNotificationContainer from "$lib/notifications/DNotificationContainer.svelte";
</script>

<WidgetSelector />
<Statusbar />
<DNotificationContainer />

<style>
  :root {
    background-color: black;
  }
</style>
