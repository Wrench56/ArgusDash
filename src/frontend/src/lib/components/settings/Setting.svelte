<script lang="ts">
  let status = "L";
  let cursor = "  ";
  let lock = false;

  export const api: SettingsApi = {
    update(new_status: string) {
      status = new_status;
    },
    keyPressed(event: KeyboardEvent) {
      if (lock) {
        return false;
      }

      if (event.key == "Enter") {
        lock = true;
        if (status == "L") {
          return false;
        }

        const nstatus = status == "E" ? "D" : "E";
        fetch(`/settings/${id}`, {
          method: "POST",
          headers: {
            "Content-Type": "text/html; charset=utf-8",
          },
          body: nstatus,
        }).then((response) => {
          if (response.ok) {
            status = nstatus;
            lock = false;
          } else {
            const ostatus = status;
            setTimeout(() => {
              status = ostatus;
              lock = false;
            }, 5000);
            status = "F";
          }
        });

        return true;
      }
    },
    setCursor(enable: boolean) {
      cursor = enable ? "> " : "  ";
    },
  };

  export let id: string;
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div
  class="container"
  on:click={() =>
    api.keyPressed(new KeyboardEvent("keydown", { key: "Enter" }))}
>
  <pre>
{#if status == "L"}
      {cursor}[<span id="gray">LOADING </span>]
    {:else if status == "E"}
      {cursor}[<span id="green">ENABLED </span>]
    {:else if status == "F"}
      {cursor}[<span id="red">  FAIL  </span>]
    {:else}
      {cursor}[<span id="red">DISABLED</span>]
    {/if}
</pre>
  <pre></pre>
  <slot></slot>
</div>

<style>
  #gray {
    color: dimgray;
  }

  #green {
    color: rgb(0, 255, 4);
  }

  #red {
    color: red;
  }

  pre {
    display: inline-block;
    padding: 0px;
    margin: 0px;
    font-family: monaco, Consolas, "Lucida Console", monospace;
    color: whitesmoke;
  }

  .container {
    cursor: pointer;
  }
</style>
