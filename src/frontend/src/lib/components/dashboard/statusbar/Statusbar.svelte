<script lang="ts">
  import version from "$lib/version";
  import Clock from "./Clock.svelte";
</script>

<div class="container">
  <a href="/settings">
    <pre class="version"> ArgusDash - v{version}</pre>
  </a>
  <Clock></Clock>
</div>

<style>
  .container {
    position: fixed;
    width: 100%;
    height: 18px;
    overflow: hidden;
    bottom: 0px;
    left: 0px;
    right: 0px;
    color: whitesmoke;
    font-family: monaco, Consolas, "Lucida Console", monospace;
    padding: 0px;
    background-color: #070707;
    align-items: center;
    text-align: center;
    display: inline-grid;
    column-gap: 2px;
    grid-template-columns: 180px auto;
  }

  pre {
    color: whitesmoke;
    font-family: monaco, Consolas, "Lucida Console", monospace;
    font-size: 12px;
    margin: 0px;
    position: absolute;
    top: 50%;
    transform: translate(0%, -50%);
  }

  .version {
    grid-column: 1;
    padding: 4px;
  }

  .version:hover {
    background-color: rgb(102, 153, 255);
  }
</style>
