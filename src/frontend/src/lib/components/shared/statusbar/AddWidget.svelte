<script lang="ts">
  import { showWidgetSelector } from "$lib/components/dashboard/widget.svelte";

</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div on:click={() => showWidgetSelector()}>Add widget</div>

<style>
  div {
    height: 100%;
    padding-top: 8px;
    text-align: center;
    color: whitesmoke;
    font-family: monaco, Consolas, "Lucida Console", monospace;
    font-size: 12px;
    margin: 0px;
    display: grid;
    grid-column: 6;
  }

  div:hover {
    background-color: rgb(102, 153, 255);
    cursor: pointer;
  }
</style>
