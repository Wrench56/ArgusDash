<script lang="ts">
  import Input from "$lib/components/login/Input.svelte";
  import Header from "$lib/components/login/motd/Header.svelte";
  import Motd from "$lib/components/login/motd/Motd.svelte";
  import Status from "$lib/components/login/motd/Status.svelte";
  import Version from "$lib/components/login/motd/Version.svelte";

</script>

<Header />
<Version />
<Motd />
<Status />
<Input />

<style>
  :root {
    background-color: black;
  }
</style>
