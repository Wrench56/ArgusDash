<script lang="ts">
  import { onMount } from "svelte";
  import { getSelectorVisibleRune } from "./widget.svelte";
  import WidgetItem from "./WidgetItem.svelte";
  import Box from "../shared/Box.svelte";
  import Separator from "../shared/Separator.svelte";
  import Header from "./WidgetHeader.svelte";

  let container: HTMLDivElement;
  $effect(() => {
    container.style.visibility = getSelectorVisibleRune()
      ? "visible"
      : "hidden";
    container.style.display = getSelectorVisibleRune() ? "block" : "none";
  });

  let widgets: Widget[] = $state([]);

  onMount(() => {
    fetch("/plugins/widgets")
      .then((data) => data.json())
      .then((data: Record<string, string[]>) => {
        widgets = Object.entries(data).flatMap(([plugin, names]) =>
          names.map((name) => ({ plugin, name }))
        );
      });
  });
</script>

<div class="container" bind:this={container}>
  <div class="widget-selector">
    <Box>
      <Header />
      <Separator />
      {#each widgets as widget}
        <WidgetItem {widget} />
      {/each}
    </Box>
  </div>
</div>

<style>
  .container {
    margin: -10px;
    padding: 100px;
    width: 100%;
    max-width: 100%;
    height: 100%;
    max-height: 100%;
    position: absolute;
    visibility: hidden;
    display: none;
    background-color: rgba(0, 0, 0, 0.075);
    box-sizing: border-box;
  }

  .widget-selector {
    position: relative;
    top: 100;
    left: 250;
    right: 250;
    bottom: 100;
    width: 100%;
    height: 100%;
    padding: inherit;
    box-sizing: border-box;
  }
</style>
