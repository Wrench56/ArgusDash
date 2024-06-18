<script lang="ts">
  import { onMount } from "svelte";
  import version from "$lib/version";

  let status = {
    ncu: "wait",
    npm_doct: "wait",
    npm_audit: "wait",
    version: "wait",
  };

  onMount(() => {
    fetch(`${window.location.origin}/login/status`)
      .then((response) => response.json())
      .then((responseJson) => {
        for (let entry in status) {
          status[entry] = responseJson[entry] ?? "hide";
        }
      })
      .then(() => {
        
        if (status.version != "hide") {
          fetch(`${window.location.origin}/version`)
            .then((response) => response.text())
            .then(
              (text) => status.version = (text == version) ? " ok " : "fail"
            );
        }
      });
  });
</script>

<pre>[ <span class={status.npm_doct.trim()}
    >{status.npm_doct.toUpperCase()}</span
  > ]    NPM Health</pre>
<pre>[ <span class={status.ncu.trim()}>{status.ncu.toUpperCase()}</span
  > ]    NPM Packages up-to-date</pre>
<pre>[ <span class={status.npm_audit.trim()}>{status.npm_audit.toUpperCase()}</span
  > ]    NPM Packages are not vulnerable</pre>
<pre>[ <span class={status.version.trim()}>{status.version.toUpperCase()}</span
  > ]    Version equals backend version</pre>

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

  .hide {
    color: dimgray;
  }
</style>
