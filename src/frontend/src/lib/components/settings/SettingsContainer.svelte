<script lang="ts">
  import { onMount } from "svelte";
  import Setting from "./Setting.svelte";

  let index = 0;

  /*
	  L => LOADING
		E => ENABLED
		D => DISABLED
	*/
  let settings_list: Array<SettingsApi> = [];

  onMount(() => {
    fetch("/settings/all")
      .then((response) => response.text())
      .then((responseText) => {
        let status_list = responseText.split(",");
        for (let i = 0; i < settings_list.length; i++) {
          settings_list[i].update(status_list[i]);
        }
      });
    settings_list[0].setCursor(true);
  });

  function handleKeydown(event: KeyboardEvent) {
    if (event.key === "ArrowUp" && index > 0) {
      event.preventDefault();
      settings_list[index].setCursor(false);
      --index;
      settings_list[index].setCursor(true);
    } else if (event.key === "ArrowDown" && index < settings_list.length - 1) {
      event.preventDefault();
      settings_list[index].setCursor(false);
      ++index;
      settings_list[index].setCursor(true);
    } else {
      settings_list[index].keyPressed(event);
    }
  }
</script>

<svelte:window on:keydown={handleKeydown} />

<div class="container">
  <Setting id="0" bind:api={settings_list[0]}>
    <pre>Build mode</pre>
  </Setting>
  <Setting id="1" bind:api={settings_list[1]}>
    <pre>General status on settings page</pre>
  </Setting>
</div>

<style>
  pre {
    padding: 0px;
    margin: 0px;
    display: inline-block;
    font-family: monaco, Consolas, "Lucida Console", monospace;
    color: whitesmoke;
  }

  .container {
    overflow: hidden;
  }
</style>
