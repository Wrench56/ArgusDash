<script lang="ts">
  import Box from "$lib/components/plugins/Box.svelte";
  import Header from "$lib/components/plugins/Header.svelte";
  import UrlField from "$lib/components/plugins/UrlField.svelte";
  import Separator from "$lib/components/shared/Separator.svelte";
  import Statusbar from "$lib/components/shared/statusbar/Statusbar.svelte";
  import DNotificationContainer from "$lib/notifications/DNotificationContainer.svelte";
</script>

<Box>
  <Header />
  <Separator />
  <UrlField />
</Box>

<DNotificationContainer />
<Statusbar />

<style>
  :root {
    background-color: black;
  }
</style>
