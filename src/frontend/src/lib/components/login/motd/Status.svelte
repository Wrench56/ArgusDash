<script lang="ts">
  import { onMount } from "svelte";

  let status = {
    ncu: "wait",
    npm_doct: "wait",
  };

  onMount(() => {
    fetch(`${window.location.origin}/login/status`)
      .then((response) => response.json())
      .then((responseJson) => {
        for (let entry in status) {
          status[entry] = responseJson[entry] ?? "stop";
        }
      });
  });
</script>

<pre>[ <span class={status.npm_doct.trim()}>{status.npm_doct.toUpperCase()}</span
  > ]    NPM Health</pre>
<pre>[ <span class={status.ncu.trim()}>{status.ncu.toUpperCase()}</span
  > ]    NPM Packages up-to-date</pre>

<style>
  pre {
    margin: 0px;
    font-family: monaco, Consolas, "Lucida Console", monospace;
    color: whitesmoke;
  }

  span {
    margin: 0px;
    font-family: monaco, Consolas, "Lucida Console", monospace;
  }

  .wait {
    color: dimgray;
  }

  .ok {
    color: rgb(0, 255, 4);
  }

  .fail {
    color: red;
  }

  .warn {
    color: rgb(255, 234, 0);
  }

  .stop {
    color: dimgray;
  }
</style>
