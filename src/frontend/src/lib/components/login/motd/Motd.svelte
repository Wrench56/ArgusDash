<script lang="ts">
    import { onMount } from "svelte";
    
    let motd = "Loading...";

    onMount(() => {
      fetch(`${window.location.origin}/login/motd`)
        .then(response => response.text())
        .then((responseText) => motd = responseText);
    });
</script>

<div class="motd">{@html motd}</div>

<style>
    .motd {
        margin-bottom: 20px;
        font-family: monaco, Consolas, "Lucida Console", monospace;
        color: whitesmoke;
        white-space: pre;
    }
</style>