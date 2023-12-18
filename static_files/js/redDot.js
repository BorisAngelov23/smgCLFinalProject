  function flashRedDot() {
    var dot = document.getElementById("live-dot");

    setInterval(function () {
      dot.style.visibility = (dot.style.visibility === 'visible' ? 'hidden' : 'visible');
    }, 500); // Adjust the interval (in milliseconds) to control the flashing speed
  }

  // Call the function when the page loads
  document.addEventListener("DOMContentLoaded", function() {
    flashRedDot();
  });