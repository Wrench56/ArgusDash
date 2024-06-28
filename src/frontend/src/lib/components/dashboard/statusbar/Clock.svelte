<script lang="ts">
  setInterval(showTime, 1000);

  let shour = "00";
  let smin = "00";
  let ssec = "00";
  let am_pm = "AM";

  function showTime() {
    let time = new Date();
    let hour = time.getHours();
    let min = time.getMinutes();
    let sec = time.getSeconds();
    am_pm = "AM";

    if (hour >= 12) {
      if (hour > 12) hour -= 12;
      am_pm = "PM";
    } else if (hour == 0) {
      am_pm = "AM";
    }

    shour = hour < 10 ? "0" + hour : hour.toString();
    smin = min < 10 ? "0" + min : min.toString();
    ssec = sec < 10 ? "0" + sec : sec.toString();
  }

  showTime();
</script>

<pre>
{`${shour}:${smin}:${ssec} ${am_pm}`}
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
</style>
