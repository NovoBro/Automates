console.log("Script loaded");

const newButton = document.querySelector("button.gitButton");
const helpButton = document.querySelector("button.button2");

newButton.addEventListener("click", function () {
    window.open('/github/auth/', '_blank'); 
});

helpButton.addEventListener("click", function () {
  alert("Help me");
});