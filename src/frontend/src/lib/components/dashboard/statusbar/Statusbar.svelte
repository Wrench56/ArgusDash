<script lang="ts">
  import Version from "$lib/components/dashboard/statusbar/BuildVersion.svelte";
  import Clock from "./Clock.svelte";
  import Latency from "./Latency.svelte";
  import Rebuild from "./Rebuild.svelte";
  import Fullscreen from "./Fullscreen.svelte";
</script>

<div class="container">
  <Version />
  <Rebuild />
  <Fullscreen />
  <Latency />
  <Clock />
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
    grid-template-columns: 160px 60px 80px 60px auto 100px;
  }
</style>
