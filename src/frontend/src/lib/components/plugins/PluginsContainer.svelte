<script lang="ts">
  import { onMount } from "svelte";
  import type {
    PluginStatus,
    PluginStatusContainer,
  } from "../shared/api/plugins.type";
  import Error from "./Error.svelte";
  import Plugin from "./Plugin.svelte";
  import Separator from "../shared/Separator.svelte";
  import { initEventSources, pluginStatusStream } from "../shared/api/streams";

  let plugins: Array<PluginStatus> = [];
  let error: string;

  function updatePluginsList(data: PluginStatusContainer) {
    if (data.ok == true) {
      plugins = data.plugins;
    }
  }

  onMount(() => {
    initEventSources();
    updatePluginsList(pluginStatusStream.fetch());
    const unsubscribe = pluginStatusStream.subscribe(
      (data: PluginStatusContainer) => updatePluginsList(data)
    );

    return () => {
      unsubscribe();
    };
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
