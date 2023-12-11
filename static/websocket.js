var socket = io();

socket.on("connect", function () {
  socket.emit("client-connection-ack");
});

socket.on("change_video", function (newVideoPath) {
  let videoPlayer = document.getElementById("video");
  console.log(newVideoPath);
  console.log(videoPlayer.src);
  changeVideo(newVideoPath);
});

function changeVideo(newVideoPath) {
  let videoPlayer = document.getElementById("video");
  videoPlayer.src = "videos/" + newVideoPath + ".mp4";
  videoPlayer.load();
  videoPlayer.play();
}
