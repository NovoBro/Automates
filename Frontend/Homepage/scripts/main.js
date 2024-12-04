console.log("Script loaded");
var isLoggedIn = localStorage.getItem("isLoggedIn") ?? false;
localStorage.setItem("isLoggedIn", isLoggedIn);
if (isLoggedIn === "true") {
    console.log("User is logged in!");
}
else { console.log("User is not logged in!"); }

const newButton = document.querySelector("button.button1");
const loginButton = document.querySelector("button.loginButton");
const signupButton = document.querySelector("button.signupButton");
const accountButton = document.querySelector("button.accountButton");
const helpButton = document.querySelector("button.button2");

if(isLoggedIn === "false"){
    signupButton.style.display = "inline";
    loginButton.style.display = "inline";
    console.log("hide");
  }
else{
  accountButton.style.display = "inline";
  newButton.style.display = "block";
  console.log("display");
}

newButton.addEventListener("click", function () {
  window.open(
    "../Text-Gen/index.html", "_blank");
});

loginButton.addEventListener("click", function () {
    window.open("../Sign-In/index.html", "_self");
});

signupButton.addEventListener("click", function () {
    window.open("../Sign-Up/index.html", "_self");
});

accountButton.addEventListener("click", function () {
  window.open("../Accounts/index.html", "_self");
});

helpButton.addEventListener("click", function () {
  alert("Help me");
});