<script lang="ts">
  import Statusbar from "$lib/components/dashboard/Statusbar.svelte";
import Header from "$lib/components/login/motd/Header.svelte";
  import Motd from "$lib/components/login/motd/Motd.svelte";
  import Status from "$lib/components/login/motd/Status.svelte";
  import Version from "$lib/components/login/motd/Version.svelte";

  import Box from "$lib/components/settings/Box.svelte";
	import SettingsHeader from "$lib/components/settings/Header.svelte";
  import Separator from "$lib/components/settings/Separator.svelte";
  import SettingsContainer from "$lib/components/settings/SettingsContainer.svelte";

</script>

<div class="status">
	<Header />
	<Version />
	<Motd />
	<Status />
</div>

<Box>
	<SettingsHeader />
	<Separator />
	<SettingsContainer />
</Box>
<Statusbar />

<style>
	:root {
		background-color: black;
	}

	.status {
		float: left;
		overflow: hidden;
		width: 550px;
	}
</style>
