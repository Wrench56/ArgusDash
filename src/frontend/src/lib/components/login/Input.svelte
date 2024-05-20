<script lang="ts">
  import { onMount } from "svelte";

  let username = "";
  let password = "";
  let usernameActive = true;
  let usernameInput: HTMLInputElement;
  let passwordInput: HTMLInputElement;

  onMount(() => {
    usernameInput.focus()
  });

  function handleKeydown(event: KeyboardEvent) {
    if (event.key === "ArrowDown" || event.key === "ArrowUp") {
      /* Ignore scroll */
      event.preventDefault();
      (usernameActive) ? passwordInput.focus() : usernameInput.focus();
    } else if (event.key === "Enter") {
      (usernameActive) ? passwordInput.focus() : authenticate();
    }
  }

  function authenticate() {}
</script>

<svelte:window
  on:keydown={handleKeydown}
/>
<p>=======================[ login ]=======================</p>
<label for="username">username></label>
<input
  type="text"
  id="username"
  bind:this={usernameInput}
  bind:value={username}
  on:focus={() => usernameActive = true}
>
<br>
<label for="password">password></label>
<input
  type="password"
  id="password"
  bind:this={passwordInput}
  bind:value={password}
  on:focus={() => usernameActive = false}
>


<style>
  p {
    margin: 10px 0px 0px 0px;
    font-family: monaco, Consolas, "Lucida Console", monospace;
    color: whitesmoke;
  }

  label {
    font-family: monaco, Consolas, "Lucida Console", monospace;
    color: whitesmoke;
    font-size: 16px;
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
    width: 396px;
  }
  input:focus {
    outline: none;
  }

</style>
