<script lang="ts">
  import Statusbar from "$lib/components/shared/statusbar/Statusbar.svelte";
  import Header from "$lib/components/login/motd/Header.svelte";
  import Motd from "$lib/components/login/motd/Motd.svelte";
  import Status from "$lib/components/login/motd/Status.svelte";
  import Version from "$lib/components/login/motd/Version.svelte";

  import Box from "$lib/components/settings/Box.svelte";
  import SettingsHeader from "$lib/components/settings/Header.svelte";
  import Separator from "$lib/components/shared/Separator.svelte";
  import SettingsContainer from "$lib/components/settings/SettingsContainer.svelte";
  import DNotificationContainer from "$lib/notifications/DNotificationContainer.svelte";
</script>

<!--STATUS_IN_SETTINGS-->
<div class="status">
  <Header />
  <Version />
  <Motd />
  <Status />
</div>
<!--END-->

<Box>
  <SettingsHeader />
  <Separator />
  <SettingsContainer />
</Box>
<Statusbar />
<DNotificationContainer />

<style>
  :root {
    background-color: black;
  }

/*STATUS_IN_SETTINGS*/
  .status {
    float: left;
    overflow: hidden;
    width: 550px;
  }
  /*END*/
</style>
