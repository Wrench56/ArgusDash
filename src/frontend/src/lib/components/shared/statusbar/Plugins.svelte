<script lang="ts">
  import { onMount } from "svelte";

  let out_of: string = "";
  let status: string = "success";
  let content: string = "LOAD*";
  onMount(() => {
    fetch("/plugins/status")
      .then((response) => response.json())
      .then((responseJson) => {
        if (responseJson.ok == true) {
          status = "success";
          out_of = `/${responseJson.plugins.length}`;
          content = responseJson.plugins.length;
        } else {
          status = "failure";
          out_of = "";
          content = "ERROR";
        }
      });
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
