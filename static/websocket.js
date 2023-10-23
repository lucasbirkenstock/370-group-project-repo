var socket = io();

socket.on("connect", function () {
  socket.emit("client-connection-ack");
});

socket.on("change_video", function (newVideoPath) {
  let videoPlayer = document.getElementById("video");
  videoPlayer.src = newVideoPath;
  videoPlayer.load();
  videoPlayer.play();
});

document
  .getElementById("changeVideoButton")
  .addEventListener("click", function () {
    socket.emit("change_video");
  });

video.addEventListener("play", (event) => {
  socket.emit("start_headband");
});
