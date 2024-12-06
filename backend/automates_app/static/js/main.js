document.addEventListener("DOMContentLoaded", function () {
    console.log("Script loaded");
  
    // Get form elements
    const generateButton = document.querySelector('.button1');
    const accountButton = document.querySelector("button.login");
    const audienceDrop = document.getElementById("audience");
    const styleDrop = document.getElementById("style");
    const toneDrop = document.getElementById("tone");
  
    const audienceTextBox = document.getElementById("audienceTextBox");
    const styleTextBox = document.getElementById("styleTextBox");
    const toneTextBox = document.getElementById("toneTextBox");
    const generatedTextArea = document.getElementById("generated");
  
    // Ensure accountButton exists before adding event listener
    if (accountButton) {
      accountButton.addEventListener("click", function () {
        window.open("../Accounts/index.html", "_blank");
      });
    }
  
    // Disable the textboxes by default
    if (audienceTextBox && styleTextBox && toneTextBox) {
      audienceTextBox.disabled = true;
      styleTextBox.disabled = true;
      toneTextBox.disabled = true;
    }
  
    // Handle dropdown changes (display 'Other' text box when 'Other' is selected)
    function handleAudienceChange() {
      const audience = audienceDrop.value;
      if (audience === "other") {
        audienceTextBox.disabled = false;  // Enable textbox when "Other" is selected
      } else {
        audienceTextBox.disabled = true;   // Disable textbox otherwise
      }
    }
  
    function handleStyleChange() {
      const style = styleDrop.value;
      if (style === "other") {
        styleTextBox.disabled = false;  // Enable textbox when "Other" is selected
      } else {
        styleTextBox.disabled = true;   // Disable textbox otherwise
      }
    }
  
    function handleToneChange() {
      const tone = toneDrop.value;
      if (tone === "other") {
        toneTextBox.disabled = false;  // Enable textbox when "Other" is selected
      } else {
        toneTextBox.disabled = true;   // Disable textbox otherwise
      }
    }
  
    // Initialize the dropdowns based on the current selections
    if (audienceDrop) handleAudienceChange();
    if (styleDrop) handleStyleChange();
    if (toneDrop) handleToneChange();
  
    // Add event listeners to handle dropdown changes
    if (audienceDrop) audienceDrop.addEventListener("change", handleAudienceChange);
    if (styleDrop) styleDrop.addEventListener("change", handleStyleChange);
    if (toneDrop) toneDrop.addEventListener("change", handleToneChange);
  
    // Ensure generateButton exists before adding event listener
    if (generateButton) {
      generateButton.addEventListener("click", function () {
        let generatedText = "";
  
        // Get values from form fields
        const description = document.getElementById("description").value;
        const audience = audienceDrop.value === "other" ? audienceTextBox.value : audienceDrop.value;
        const style = styleDrop.value === "other" ? styleTextBox.value : styleDrop.value;
        const tone = toneDrop.value === "other" ? toneTextBox.value : toneDrop.value;
        const hashtags = document.getElementById("hashtags").value;
  
        // Construct the generated text
        generatedText += `Description: ${description}\n\n`;
        generatedText += `Audience: ${audience}\n`;
        generatedText += `Style: ${style}\n`;
        generatedText += `Tone: ${tone}\n`;
        generatedText += `Hashtags: ${hashtags}\n`;
  
        // Set the generated text in the generated text area
        if (generatedTextArea) {
          generatedTextArea.value = generatedText;
        }
      });
    }
  
    // Sample JSON for repositories (for generating repository buttons)
    // var text = `{
    //   "repositories": [
    //     {"name": "Ballistic missile", "date created": "1986-12-14", "description": "Fun for the whole family!"},
    //     {"name": "Test repo", "date created": "1986-12-14", "description": "description100!"},
    //     {"name": "I can't believe it's not butter!", "date created": "1986-12-14", "description": "Friday"},
    //     {"name": "Super Computer Sim", "date created": "1986-12-14", "description": "holy mackeral"},
    //     {"name": "test repo 2", "date created": "1986-12-14", "description": "qwerty"}
    //   ]
    // }`;
    async function fetchRepositories() {
      try {
          const grabToken = new URLSearchParams(window.location.search);
          const token = grabToken.get('token');
          const response = await fetch(`/api/user-repos/?token=${token}`);
          
          if (!response.ok) {
              throw new Error(`Error fetching repositories: ${response.status}`);
          }

          const repositories = await response.json();
          console.log("Fetched repositories:", repositories);

          if (btnGroup) {
              btnGroup.innerHTML = '';
          }

          let activeButton = null;

          repositories.forEach(repo => {
              const button = document.createElement('button');
              button.textContent = repo.name;

              button.addEventListener('click', function () {
                  if (activeButton) {
                      activeButton.style.backgroundColor = '';
                  }

                  button.style.backgroundColor = "#2d343c";
                  activeButton = button;

                  console.log("Current repository:", repo);
                  alert(`Description: ${repo.description}`);
              });

              if (btnGroup) {
                  btnGroup.appendChild(button);
              }
          });
      } catch (error) {
          console.error("Error fetching repositories:", error);
      }
  }

  fetchRepositories();
  
    const obj = JSON.parse(text);
    const repositories = obj.repositories; // Extract the repositories array
  
    // Select the button group container
    const btnGroup = document.querySelector('.btn-group');
  
    // Remove any existing button(s) to start fresh
    if (btnGroup) {
      btnGroup.innerHTML = '';
    }
  
    let activeButton = null; // Variable to track the currently active button
  
    // Create and append a button for each repository
    repositories.forEach(repo => {
      const button = document.createElement('button');
      button.textContent = repo.name; // Set button name
  
      // Add click event listener to show the description in an alert
      button.addEventListener('click', function () {
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
      if (btnGroup) {
        btnGroup.appendChild(button);
      }
    });
  });
  
  