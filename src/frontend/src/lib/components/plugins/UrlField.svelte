<script lang="ts">
  import { onMount } from "svelte";

  let pluginUrl: string;
  let pluginUrlInput: HTMLInputElement;

  onMount(() => {
    pluginUrlInput.focus();
  });

  function handleKeydown(event: KeyboardEvent) {
    if (event.key === "Enter") {
      fetch("/plugins", {
        method: "POST",
        headers: {
          "Content-Type": "application/json; charset=utf-8",
        },
        body: JSON.stringify({
          url: pluginUrl,
        }),
      });
    }
  }
</script>

<svelte:window on:keydown={handleKeydown} />

<div class="grid">
  <label for="plugin-url">Plugin.toml URL></label>
  <input
    type="text"
    id="plugin-url"
    bind:this={pluginUrlInput}
    bind:value={pluginUrl}
  />
</div>

<style>
  .grid {
    display: flex;
  }

  label {
    font-family: monaco, Consolas, "Lucida Console", monospace;
    color: whitesmoke;
    font-size: 16px;
    flex: 0 0 150px;
  }

  input {
    border: none;
    background: none;
    font-family: monaco, Consolas, "Lucida Console", monospace;
    color: whitesmoke;
    outline: none;
    caret: whitesmoke block;
    margin: 0px;
    font-size: 16px;
    flex-grow: 1;
  }

  input:focus {
    outline: none;
  }
</style>
