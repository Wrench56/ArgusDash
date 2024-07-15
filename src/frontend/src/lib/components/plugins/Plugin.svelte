<script lang="ts">
  import type { PluginStatus } from "../shared/api/plugins.type";

  export let data: PluginStatus;
</script>

{#if data.status}
  <pre class="online">[<span style="color: rgb(0, 255, 0);">ONLINE</span
    >]   {data.name}</pre>
{:else}
  <pre class="offline"><span style="color: red;">OFFLINE</span
    >]    {data.name}</pre>
{/if}

<style>
  pre {
    white-space: pre;
    font-family: monaco, Consolas, "Lucida Console", monospace;
    color: whitesmoke;
    font-size: 16px;
    margin: 0px;
  }

  span {
    font-family: monaco, Consolas, "Lucida Console", monospace;
  }
</style>
