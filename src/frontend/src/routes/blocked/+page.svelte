<script lang="ts">
  function redirect() {
    window.location.href = "/";
  }
</script>

<svelte:window on:keydown|preventDefault={redirect} />

<h1>Blocked</h1>
<p>You are not logged in!
Press any key to be redirected.</p>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
<p class="redirect" on:click={() => redirect()}>Login here</p>

<style>
  h1 {
    color: whitesmoke;
    font-family: monaco, Consolas, "Lucida Console", monospace;
  }

  p {
    color: whitesmoke;
    font-family: monaco, Consolas, "Lucida Console", monospace;
    white-space: pre-line;
  }

  .redirect {
    margin-top: 0px;
    color: rgb(102, 153, 255);
    font-family: monaco, Consolas, "Lucida Console", monospace;
    cursor: pointer;
  }

  :root {
    background-color: black;
  }
</style>
