<script lang="ts">
  export let widget: Widget;
</script>

<div class="container">
  <pre><span style="color: rgb(0, 255, 0);">{widget.name}</span> from plugin <span style="color: rgb(0, 255, 0);">{widget.plugin.replace('_', '-')}</span></pre>
</div>

<style>
  pre {
    color: whitesmoke;
  }

  .container {
    background-color: black;
  }

  .container:hover {
    background-color: rgb(102, 153, 255);
    cursor: pointer;
  }
</style>
