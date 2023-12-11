window.onload = function () {
  fetch("/images")
    .then((response) => response.json())
    .then((data) => {
      const container = document.getElementById("image-container");
      data.forEach((img) => {
        const imgContainer = document.createElement("div");
        imgContainer.className = "imgContainer";
        const imgElement = document.createElement("img");
        imgElement.src = img;
        imgElement.classList.add("thumbnail");
        tokens = img.split("/");
        name = tokens.pop();
        name = name.replace(".png", "");
        imgElement.id = img;
        const p = document.createElement("p");
        p.textContent = name;
        imgContainer.appendChild(imgElement);
        imgContainer.appendChild(p);
        //imgElement.onclick = changeVideo(name);

        //imgContainer.addEventListener('click', changeVideo(name));
        function createClickListener(name) {
          return function (event) {
            let videoPlayer = document.getElementById("video");
            videoPlayer.src = "videos/edu/" + name + ".mp4";
            videoPlayer.load();
            videoPlayer.play();
          };
        }
        imgContainer.addEventListener("click", createClickListener(name));
        container.appendChild(imgContainer);
      });
    });
};

document.getElementById("toggleButton").addEventListener("click", function () {
  var thumbnailRow = document.getElementById("image-container");
  var thumb = document.getElementById("thumb");
  if (thumbnailRow.style.display === "none") {
    thumbnailRow.style.display = "flex"; // or your original display type
    thumb.style.display = "none";
  } else {
    thumbnailRow.style.display = "none";
    thumb.style.display = "flex";
    switchBackToThumb();
  }
});
