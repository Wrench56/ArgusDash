function requestFullscreen(): void {
	const element = document.documentElement;
  if (element.requestFullscreen) {
    element.requestFullscreen();
  } else if (element.mozRequestFullScreen) {
    element.mozRequestFullScreen();
  } else if (element.webkitRequestFullscreen) {
    element.webkitRequestFullscreen();
  } else if (element.msRequestFullscreen) {
    element.msRequestFullscreen();
  }
}

function exitFullscreen(): void {
  if (document.exitFullscreen) {
    document.exitFullscreen();
  } else if (document.mozCancelFullScreen) {
    document.mozCancelFullScreen();
  } else if (document.webkitExitFullscreen) {
    document.webkitExitFullscreen();
  } else if (document.msExitFullscreen) {
    document.msExitFullscreen();
  }
}

function isFullscreen(): boolean {
  return (
    document.fullscreenElement != null ||
    document.mozFullScreenElement != null ||
    document.webkitFullscreenElement != null ||
    document.msFullscreenElement != null
  );
}

export function toggleFullscreen() {
    if (!isFullscreen()) {
      requestFullscreen();
		} else {
			exitFullscreen()
		}
}
