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

  async function authenticate() {
    sha256(password).then(password_sha => {
      fetch(`${window.location.origin}/auth`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json; charset=utf-8'
        },
        body: JSON.stringify({
          username: username,
          password: password_sha
        })
      }).then((response) => {
        /* TODO: Notify user if there is a problem */
        if (response.ok) {
          window.location.replace(`${window.location.origin}/dashboard`);
        }
      });
    });
  }

  /* Source: https://stackoverflow.com/questions/18338890/ */
  async function sha256(data: string) {
    const msgBuffer = new TextEncoder().encode(data);                    
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
    const hashArray = Array.from(new Uint8Array(hashBuffer));                 
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  }

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
