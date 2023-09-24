document.addEventListener("DOMContentLoaded", function () {
  const loadingProgress = document.getElementById("loading-progress");
  const content = document.getElementById("content");

  // Simulate loading
  setTimeout(() => {
      loadingProgress.style.display = "none";
      content.style.display = "block";
  }, 1000);
});
