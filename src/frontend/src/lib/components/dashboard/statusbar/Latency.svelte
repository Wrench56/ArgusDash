<script lang="ts">
  import { onMount } from "svelte";
  /*
        -1 => init
        -2 => error

        Positive values are the actual latency in ms
    */
  let latency: number = -1;

  onMount(() => {
    ping();
  });

  setInterval(ping, 3000);
  function ping() {
    let started: number;
    let http = new XMLHttpRequest();

    http.onreadystatechange = function () {
      if (http.readyState == 1) {
        /* OPENED */
        started = new Date().getTime();
      }
      if (http.readyState == 4) {
        /* DONE */
        latency = new Date().getTime() - started;
      }
    };

    http.open("GET", "/ping", true);
    try {
      http.send(null);
    } catch (exception) {}
  }

  function latencyColor(latency: number) {
    if (latency < 10) {
      return "great";
    } else if (latency < 20) {
      return "decent";
    } else if (latency < 50) {
      return "average";
    } else if (latency < 100) {
      return "poor";
    }

    return "terrible";
  }

  function formatLatency(latency: number) {
    let latencyStr: string;
    if (latency < 0) {
      switch (latency) {
        case -1:
          latencyStr = "INIT  ";
          break;
        case -2:
          latencyStr = "ERROR ";
          break;
        default:
          latencyStr = "UNKWN ";
          break;
      }
    } else {
      latencyStr = `${latency}`.padStart(4, " ");
    }

    return latencyStr;
  }
</script>

<pre>
  <span id={latencyColor(latency)}>{formatLatency(latency)}<span id="normal"> ms</span></span>
</pre>

<style>
  pre {
    color: whitesmoke;
    font-family: monaco, Consolas, "Lucida Console", monospace;
    font-size: 12px;
    margin: 0px;
    display: grid;
    grid-column: 4;
  }

  span {
    display: inline-block;
  }

  #great {
    color: rgb(0, 255, 0);
  }

  #decent {
    color: rgb(102, 255, 0);
  }

  #average {
    color: rgb(166, 255, 0);
  }

  #poor {
    color: rgb(255, 255, 0);
  }

  #terrible {
    color: red;
  }

	#normal {
		color: whitesmoke;
	}
</style>
