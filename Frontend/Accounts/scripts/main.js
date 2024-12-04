console.log("Script loaded");

const newButton = document.querySelector("button.gitButton");
const signOutButton = document.querySelector("button.signOutButton");

newButton.addEventListener("click", function () {
  window.open('/github/auth/', '_blank'); 
});

signOutButton.addEventListener("click", function () {
  localStorage.setItem("isLoggedIn", "false");
  window.open("../Homepage/index.html", "_self");
});