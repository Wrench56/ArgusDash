<script lang="ts">
  import version from "$lib/version";
</script>

<a href="/settings">
  <pre class="version"> ArgusDash - v{version}</pre>
</a>

<style>
  pre {
    color: whitesmoke;
    font-family: monaco, Consolas, "Lucida Console", monospace;
    font-size: 12px;
    margin: 0px;
  }

  .version {
    grid-column: 1;
    padding: 4px;
  }

  a {
    flex-grow: 1;
    text-decoration: none;
  }

  .version:hover {
    background-color: rgb(102, 153, 255);
  }
</style>
