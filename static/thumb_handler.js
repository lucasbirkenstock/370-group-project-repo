var engVideoSources = [];
var disVideoSources = [];
var currentVideoSources = [];
function toggleThumbs(x) {
  x.classList.toggle("fa-thumbs-down");
}
function shuffleArray(array) {
  for (var i = array.length - 1; i > 0; i--) {
    var j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
}

document.addEventListener("DOMContentLoaded", function () {
  fetchVideos();
});

function fetchVideos() {
  fetch("/get-all-video-paths")
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok for English videos");
      }
      return response.json();
    })
    .then((data) => {
      let list1 = data[0];
      let list2 = data[1];
      console.log(list1);
      console.log(list2);

      engVideoSources = list1;
      disVideoSources = list2;

      shuffleArray(engVideoSources);
      shuffleArray(disVideoSources);
      currentVideoSources = engVideoSources;

      document.getElementById("video").src = engVideoSources[0];
    })
    .catch((error) => {
      console.error("Problem with fetch operation for English videos:", error);
    });
}

// Variable to track if thumbs-down was clicked
var thumbsDownClicked = false;

// Thumbs-up/thumbs-down icon toggle function
function toggleThumbs(x) {
  var videoElement = document.getElementById("video");

  // If currently thumbs-up, switch to thumbs-down
  if (x.classList.contains("fa-thumbs-up")) {
    currentVideoSources = disVideoSources;
    thumbsDownClicked = true; // Mark that thumbs-down was clicked
  } else if (x.classList.contains("fa-thumbs-down")) {
    // If currently thumbs-down, switch to thumbs-up
    currentVideoSources = engVideoSources;
    thumbsDownClicked = false; // Reset the flag when thumbs-up is clicked
  }

  // Rotate the video sources array
  currentVideoSources.push(currentVideoSources.shift());

  // Set the new video source to the video element
  videoElement.src = currentVideoSources[0];

  // Toggle the class
  x.classList.toggle("fa-thumbs-up");
  x.classList.toggle("fa-thumbs-down");

  // Play the new video
  videoElement.play();
}

// Function to play the next video when the current one ends
function play_next() {
  var videoElement = document.getElementById("video");
  var thumbsIcon = document.querySelector(".fa");

  // If thumbs-down was clicked, switch back to eng_vids
  if (thumbsDownClicked) {
    thumbsDownClicked = false; // Reset the flag
    currentVideoSources = engVideoSources;

    // Toggle the class to switch from thumbs-down to thumbs-up
    thumbsIcon.classList.toggle("fa-thumbs-up");
    thumbsIcon.classList.toggle("fa-thumbs-down");
  }

  // Rotate the video sources array
  currentVideoSources.push(currentVideoSources.shift());

  // Set the new video source to the video element
  videoElement.src = currentVideoSources[0];

  // Play the new video
  videoElement.play();
}

// Event listener for the "ended" event of the video
document.getElementById("video").addEventListener("ended", play_next);

video.addEventListener("play", (event) => {
  play_start();
});

function switchBackToThumb() {
  currentVideoSources = engVideoSources;
  var thumbsIcon = document.querySelector(".fa");
  thumbsIcon.classList.toggle("fa-thumbs-up");
  thumbsIcon.classList.toggle("fa-thumbs-down");
  thumbsIcon.classList.toggle("fa-thumbs-up");
  thumbsIcon.classList.toggle("fa-thumbs-down");
}

// video.addEventListener("stop", (event) =>{
// 	play_stop();
// });
