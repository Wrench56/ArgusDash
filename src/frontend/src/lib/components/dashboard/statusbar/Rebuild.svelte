<script lang="ts">
  function rebuild() {
    fetch("/rebuild", { method: "POST" }).then((response) => {
      if (response.ok) {
        response.text().then((text) => {
          if (text.startsWith("REBUILT")) {
            location.reload();
          }
        });
      }
    });
  }
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div on:click={() => rebuild()}>
  Rebuild
</div>

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
    grid-column: 3;
  }

  div:hover {
    background-color: rgb(102, 153, 255);
    cursor: pointer;
  }
</style>
