<script lang="ts">
  import { type Writable } from "svelte/store";
  import { NotificationState, type NotificationWrapper } from "./notify";

  export let wrapper: NotificationWrapper;
  let state: Writable<NotificationState> = wrapper.data.state;
  $: wrapper ? refresh() : null;
  function refresh() {
    state = wrapper.data.state;

    if ($state == NotificationState.Appear) {
      /* Begin transition */
      setTimeout(() => {
        wrapper.data.state.set(NotificationState.Alive);
        setTimeout(() => {
          wrapper.data.state.set(NotificationState.Disappear);
          setTimeout(() => {
            wrapper.data.after();
            wrapper.data.state.set(NotificationState.Dead);
          }, 500);
        }, wrapper.data.duration || 2000);
      }, 1);
    }
  }

  $: state ? console.log("X" + $state) : null;
</script>

<div class="container container-{$state} {wrapper.data.priority}">
  <h1>{wrapper.notification.title}</h1>
  <pre>{wrapper.notification.body}</pre>
</div>

<style>
  .container {
    border-radius: 8px;
    width: 240px;
    height: 90px;
    padding: 4px;
    margin: 8px;
    background-color: #010101;
    overflow: hidden;
  }

  .container-appear {
    opacity: 0;
    transform: rotateX(-90deg);
    transition: all 0.5s cubic-bezier(0.36, -0.64, 0.34, 1.76);
  }

  .container-alive {
    opacity: 1;
    transform: none;
    transition: all 0.5s cubic-bezier(0.36, -0.64, 0.34, 1.76);
  }

  .container-disappear {
    opacity: 1;
    transform: rotateX(90deg);
    transition: all 0.5s cubic-bezier(0.36, -0.64, 0.34, 1.76);
  }

  .container-dead {
    opacity: 0;
  }

  h1 {
    font-family: monaco, Consolas, "Lucida Console", monospace;
    color: whitesmoke;
    font-size: 18px;
    text-align: left;
    margin: 6px 0px 0px 10px;
  }

  pre {
    font-family: monaco, Consolas, "Lucida Console", monospace;
    color: whitesmoke;
    font-size: 12px;
    text-align: left;
    margin: 6px 0px 0px 16px;
    white-space: pre-wrap;
    white-space: -moz-pre-wrap;
    white-space: -pre-wrap;
    white-space: -o-pre-wrap;
    word-wrap: break-word;
  }

  .default {
    border: 2px solid slategray;
  }

  .info {
    border: 2px solid rgb(102, 153, 255);
  }

  .system {
    border: 2px solid rgb(0, 255, 4);
  }
</style>
