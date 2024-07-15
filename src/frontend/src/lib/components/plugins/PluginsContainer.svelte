<script lang="ts">
  import { onMount } from "svelte";
  import type { PluginStatus } from "../shared/api/plugins.type";
  import Error from "./Error.svelte";
  import Plugin from "./Plugin.svelte";
  import Separator from "../shared/Separator.svelte";

  let plugins: Array<PluginStatus> = [];
  let error: string;

  onMount(() => {
    fetch("/plugins/status")
      .then((response) => response.json())
      .then((responseJson) => {
        if (responseJson.ok == true) {
          plugins = responseJson.plugins;
        } else {
          plugins = [];
          error = responseJson.error;
        }
      });
  });
</script>


<Separator />
{#if plugins.length == 0}
  <Error {error} />
{/if}
{#each plugins as plugin}
  <Plugin data={plugin} />
{/each}

<style>
</style>
