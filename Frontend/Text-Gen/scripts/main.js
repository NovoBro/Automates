console.log("Script loaded");

const accountButton = document.querySelector("button.login");
const helpButton = document.querySelector("button.button2");
const generateButton = document.querySelector("button.button1");
const copyButton = document.querySelector("button.copyButton");
var settings = [];
var description;
var hashtags;

copyButton.addEventListener("click", function () {
  copyFrom = document.getElementById("descriptionOutput");

  copyFrom.select();

  navigator.clipboard.writeText(copyFrom.value);

  document.getSelection().collapseToEnd();

  alert("Copied to Clipboard!");
});

accountButton.addEventListener("click", function () {
  window.open(
    "../Accounts/index.html", "_blank");
});

/*
helpButton.addEventListener("click", function () {
  alert("Help me");
});
*/

generateButton.addEventListener("click", function () {
  event.preventDefault(); 
  settings = [];
  description = document.getElementById("description").value;
  hashtags = document.getElementById("hashtags").value;
  var a = audience;
  var s  = style;
  var t = tone;
  if(audience === "Other"){
    a = audienceOther;
  }
  if(style === "Other"){
    s = styleOther;
  }
  if(tone === "Other"){
    t = toneOther;
  }
  settings.push(description, a, s, t, hashtags);
  console.log(settings);
  sleep(5000);
  document.getElementById("descriptionOutput").value = `🚀 Excited to share Automates, my latest project designed to simplify LinkedIn content creation for developers!

What is Automates?
Automates is a fully functional platform that generates LinkedIn posts based on your GitHub repositories. With an intuitive frontend and a robust backend, the website leverages ChatGPT to create polished, professional posts tailored to showcase your work.

Whether you're looking to share a recent project, highlight key milestones, or present your achievements, Automates helps you turn your code into compelling stories for LinkedIn.

This project was an incredible learning experience, combining full-stack development, API integration, and AI-driven automation.


👉 Check it out: https://github.com/NovoBro/Automates
I’d love to hear your thoughts or feedback!

#LinkedIn`;
console.log("Got this far!")
});

const audienceDrop = document.getElementById("audience");
var audience;
var audienceOther = document.getElementById("audienceTextBox").value;
const styleDrop = document.getElementById("style");
var style;
var styleOther = document.getElementById("styleTextBox").value;
const toneDrop = document.getElementById("tone");
var tone;
var toneOther = document.getElementById("toneTextBox").value;

function handleAudienceChange() {
  audience = audienceDrop.options[audienceDrop.selectedIndex].text;
  console.log("Selected audience:", audience);
  
  if (audience === "Other") {
    audienceTextBox.style.display = "block";
  } else {
    audienceTextBox.style.display = "none";
  }
}

function handleStyleChange() {
  style = styleDrop.options[styleDrop.selectedIndex].text;
  console.log("Selected style:", style);
  
  if (style === "Other") {
    styleTextBox.style.display = "block";
  } else {
    styleTextBox.style.display = "none";
  }
}

function handleToneChange() {
  tone = toneDrop.options[toneDrop.selectedIndex].text;
  console.log("Selected tone:", tone);
  
  if (tone === "Other") {
    toneTextBox.style.display = "block";
  } else {
    toneTextBox.style.display = "none";
  }
}

var text = `{
  "repositories": [
    {"name": "Automates", "date created": "1986-12-14", "description": "Text-generator for LinkedIn posts"},
    {"name": "Test repo", "date created": "1986-12-14", "description": "description100!"},
    {"name": "I can't believe it's not butter!", "date created": "1986-12-14", "description": "Friday"},
    {"name": "Super Computer Sim", "date created": "1986-12-14", "description": "holy mackeral"},
    {"name": "test repo 2", "date created": "1986-12-14", "description": "qwerty"}
  ]
}`;

// Parse the JSON text
const obj = JSON.parse(text);
const repositories = obj.repositories; // Extract the repositories array

// Select the button group container
const btnGroup = document.querySelector('.btn-group');

// Remove any existing button(s) to start fresh
btnGroup.innerHTML = '';

let activeButton = null; // Variable to track the currently active button

var repository;
// Create and append a button for each repository
repositories.forEach(repo => {
  const button = document.createElement('button');
  button.textContent = repo.name; // Set button name

  // Add click event listener to show the description in an alert
  button.addEventListener('click', function () {
    event.preventDefault();
    // Reset color of the previously active button
    if (activeButton) {
      activeButton.style.backgroundColor = ''; // Reset to default color
    }

    // Highlight the currently clicked button
    button.style.backgroundColor = "#2d343c";
    activeButton = button; // Update the active button reference
    repository = repo;
    console.log("Current repository: ", repository.name);
    // Show repository description
    alert(repo.description);
  });

  // Append the button to the button group
  btnGroup.appendChild(button);
});

// Check the initial selection on page load
handleAudienceChange();
handleStyleChange();
handleToneChange();

// Add event listener to handle dropdown changes
audienceDrop.addEventListener("change", handleAudienceChange);
styleDrop.addEventListener("change", handleStyleChange);
toneDrop.addEventListener("change", handleToneChange);


function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}