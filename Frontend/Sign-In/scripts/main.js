console.log("Script loaded");

const submit = document.querySelector('input[type="submit"]');

submit.addEventListener("click", function () {
  event.preventDefault();
  localStorage.setItem("isLoggedIn", "true");
  console.log("User is logged in!");
  window.open(
    "../Homepage/index.html", "_self");
});
