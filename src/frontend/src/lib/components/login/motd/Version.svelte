<script lang="ts">
    import version from "$lib/version";
    /* Update this */
    const HEADER_LENGTH = 55;

    const formatted_version = `${"".padStart(HEADER_LENGTH-version.length-1, " ")}v${version}`;
</script>

<pre>{formatted_version}</pre>

<style>
    pre {
        margin: 0px 0px 16px 0px;
        font-family: monaco, Consolas, "Lucida Console", monospace;
        color: dimgray;
    }
</style>