<script lang="ts">
  import { onMount } from "svelte";
  import { initEventSources, pluginStatusStream } from "../api/streams";
  import type { PluginStatusContainer } from "../api/plugins.type";

  let out_of: string = "";
  let status: string = "success";
  let content: string = "LOAD*";

  function updateStatus(data: PluginStatusContainer) {
    if (data.ok) {
      status = "success";
      out_of = `/${data.plugins.length}`;
      content = data.plugins.length.toString();
    } else {
      status = "failure";
      out_of = "";
      content = "ERROR";
    }
  }

  onMount(() => {
    initEventSources();
    updateStatus(pluginStatusStream.fetch());
    const unsubscribe = pluginStatusStream.subscribe(
      (data: PluginStatusContainer) => updateStatus(data)
    );

    return () => {
      unsubscribe();
    };
  });
</script>

<a href="/plugins">
  <pre class="plugins">Plugins: <span id={status}>{content}</span>{out_of}</pre>
</a>

<style>
  pre {
    color: whitesmoke;
    font-family: monaco, Consolas, "Lucida Console", monospace;
    font-size: 12px;
    margin: 0px;
  }

  .plugins {
    grid-column: 4;
    padding: 4px;
  }

  .plugins:hover {
    background-color: rgb(102, 153, 255);
  }

  #success {
    color: rgb(0, 255, 0);
  }

  #failure {
    color: red;
  }

  a {
    flex-grow: 1;
    text-decoration: none;
  }
</style>
