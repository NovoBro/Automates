console.log("Script loaded");

console.log(localStorage.getItem("isLoggedIn"));
var isLoggedIn = localStorage.getItem("isLoggedIn") ?? false;
localStorage.setItem("isLoggedIn", isLoggedIn);

const submit = document.querySelector('input[type="submit"]');

submit.addEventListener("click", function () {
  event.preventDefault();
  localStorage.setItem("isLoggedIn", "true");
  console.log("User is logged in!");
  window.open(
    "../Homepage/index.html", "_self");
});