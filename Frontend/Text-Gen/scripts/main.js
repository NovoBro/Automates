console.log("Script loaded");

const newButton = document.querySelector("button.button1");
const accountButton = document.querySelector("button.login");
const helpButton = document.querySelector("button.button2");

accountButton.addEventListener("click", function () {
  window.open(
    "../Accounts/index.html", "_blank");
});

/*
helpButton.addEventListener("click", function () {
  alert("Help me");
});
*/

const audienceDrop = document.getElementById("audience");
var audience;
var audienceOther = document.getElementById("audienceTextBox");
const styleDrop = document.getElementById("style");
var style;
var audienceOther = document.getElementById("styleTextBox");
const toneDrop = document.getElementById("tone");
var tone;
var toneOther = document.getElementById("toneTextBox");

function handleAudienceChange() {
  audience = audienceDrop.options[audienceDrop.selectedIndex].text;
  console.log("Selected audience:", audience);
  
  if (audience === "Other") {
    console.log("Display");
    audienceTextBox.style.display = "block";
  } else {
    console.log("Hide");
    audienceTextBox.style.display = "none";
  }
}

function handleStyleChange() {
  style = styleDrop.options[styleDrop.selectedIndex].text;
  console.log("Selected style:", style);
  
  if (style === "Other") {
    console.log("Display");
    styleTextBox.style.display = "block";
  } else {
    console.log("Hide");
    styleTextBox.style.display = "none";
  }
}

function handleToneChange() {
  tone = toneDrop.options[toneDrop.selectedIndex].text;
  console.log("Selected tone:", tone);
  
  if (tone === "Other") {
    console.log("Display");
    toneTextBox.style.display = "block";
  } else {
    console.log("Hide");
    toneTextBox.style.display = "none";
  }
}

// Check the initial selection on page load
handleAudienceChange();
handleStyleChange();
handleToneChange();

// Add event listener to handle dropdown changes
audienceDrop.addEventListener("change", handleAudienceChange);
styleDrop.addEventListener("change", handleStyleChange);
toneDrop.addEventListener("change", handleToneChange);
