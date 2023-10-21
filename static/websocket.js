var socket = io();

socket.on("connect", function () {
  socket.emit("my event", { data: "I'm connected!" });
});

socket.on("change_video", function (newVideoPath) {
  let videoPlayer = document.getElementById("video");
  videoPlayer.src = newVideoPath;
  videoPlayer.load();
  videoPlayer.play();
});
