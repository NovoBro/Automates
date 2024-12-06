document.addEventListener("DOMContentLoaded", function () {
    console.log("Script loaded");

    // Get form elements
    const saveButton = document.querySelector(".save-draft-button");
    const generateButton = document.querySelector(".generate-button");
    const deleteButton = document.querySelector(".delete-draft-button");
    const draftsContainer = document.querySelector(".draft-group");

    let selectedDraftId = null; // Variable to store the ID of the selected draft

    // Handle the enable/disable of the textboxes based on dropdown selections
    const audienceDrop = document.getElementById("audience");
    const styleDrop = document.getElementById("style");
    const toneDrop = document.getElementById("tone");

    const audienceTextBox = document.getElementById("audienceTextBox");
    const styleTextBox = document.getElementById("styleTextBox");
    const toneTextBox = document.getElementById("toneTextBox");

    // Enable the textboxes if "Other" is selected, and reset if not
    function toggleTextbox() {
        // Reset textboxes when switching to other options
        if (audienceDrop.value !== "other") {
            audienceTextBox.value = "";
            audienceTextBox.disabled = true;
        } else {
            audienceTextBox.disabled = false;
        }

        if (styleDrop.value !== "other") {
            styleTextBox.value = "";
            styleTextBox.disabled = true;
        } else {
            styleTextBox.disabled = false;
        }

        if (toneDrop.value !== "other") {
            toneTextBox.value = "";
            toneTextBox.disabled = true;
        } else {
            toneTextBox.disabled = false;
        }
    }

    audienceDrop.addEventListener("change", toggleTextbox);
    styleDrop.addEventListener("change", toggleTextbox);
    toneDrop.addEventListener("change", toggleTextbox);

    // Initial state
    toggleTextbox();

    // Save Draft functionality
    if (saveButton) {
        saveButton.addEventListener("click", function (event) {
            event.preventDefault(); // Prevent form submission

            const draftName = prompt("Enter a name for your draft:");
            if (!draftName) return;

            const description = document.getElementById("description").value;
            const audience = audienceDrop.value === "other" ? "" : audienceDrop.value;  // Don't save "other" text field
            const style = styleDrop.value === "other" ? "" : styleDrop.value;  // Don't save "other" text field
            const tone = toneDrop.value === "other" ? "" : toneDrop.value;  // Don't save "other" text field
            const hashtags = document.getElementById("hashtags").value;

            fetch("/save_draft/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": getCSRFToken(),
                },
                body: new URLSearchParams({
                    name: draftName,
                    description: description,
                    audience: audience,
                    style: style,
                    tone: tone,
                    hashtags: hashtags,
                }),
            })
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    alert("Draft saved successfully!");
                    loadDrafts(); // Refresh draft list
                } else {
                    alert("Failed to save draft.");
                }
            });
        });
    }

    // Generate Text and Save as Draft
    if (generateButton) {
        generateButton.addEventListener("click", function () {
            const draftName = prompt("Enter a name for your generated draft:");
            if (!draftName) return;

            let generatedText = "";

            // Get values from form fields
            const description = document.getElementById("description").value;
            const audience = audienceDrop.value === "other" ? "" : audienceDrop.value;  // Don't save "other" text field
            const style = styleDrop.value === "other" ? "" : styleDrop.value;  // Don't save "other" text field
            const tone = toneDrop.value === "other" ? "" : toneDrop.value;  // Don't save "other" text field
            const hashtags = document.getElementById("hashtags").value;

            // Construct the generated text
            generatedText += `Description: ${description}\n\n`;
            generatedText += `Audience: ${audience}\n`;
            generatedText += `Style: ${style}\n`;
            generatedText += `Tone: ${tone}\n`;
            generatedText += `Hashtags: ${hashtags}\n`;

            // Set the generated text in the generated text area
            document.getElementById("generated").value = generatedText;

            // Save the generated text as a draft
            saveDraft(generatedText, draftName);
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
  
          if (!token) {
              console.error("Authorization token is missing");
              alert("Token not found in URL. Please log in.");
              return;
          }
  
          const response = await fetch(`/repos/?token=${token}`);
  
          if (!response.ok) {
              throw new Error(`Error fetching repositories: ${response.status}`);
          }
  
          const repositories = await response.json();
          console.log("Fetched repositories:", repositories);
  
          const btnGroup = document.querySelector('.btn-group');
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
  
    const obj = JSON.parse(text);
    const repositories = obj.repositories; // Extract the repositories array
  
    // Select the button group container
    const btnGroup = document.querySelector('.btn-group');
  
    // Remove any existing button(s) to start fresh
    if (btnGroup) {
      btnGroup.innerHTML = '';

    // Function to save generated text as a draft
    function saveDraft(generatedText, draftName) {
        fetch("/save_draft/", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCSRFToken(),
            },
            body: new URLSearchParams({
                name: draftName,
                description: generatedText,
                audience: audienceDrop.value === "other" ? "" : audienceDrop.value, // Don't save "other" text field
                style: styleDrop.value === "other" ? "" : styleDrop.value, // Don't save "other" text field
                tone: toneDrop.value === "other" ? "" : toneDrop.value, // Don't save "other" text field
                hashtags: document.getElementById("hashtags").value,
            }),
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                alert("Draft saved successfully!");
                loadDrafts(); // Refresh draft list
            } else {
                alert("Failed to save draft.");
            }
        })
        .catch((error) => {
            console.error("Error saving draft:", error);
            alert("Failed to save draft.");
        });
    }

    // Handle delete draft functionality
    if (deleteButton) {
        deleteButton.addEventListener("click", function () {
            if (!selectedDraftId) {
                alert("No draft selected to delete.");
                return;
            }

            // Confirm the deletion
            if (confirm("Are you sure you want to delete this draft?")) {
                fetch(`/delete_draft/${selectedDraftId}/`, {
                    method: "DELETE",
                    headers: {
                        "X-CSRFToken": getCSRFToken(),
                    },
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert("Draft deleted successfully!");
                        loadDrafts(); // Refresh the draft list
                    } else {
                        alert("Failed to delete draft.");
                    }
                });
            }
        });
    }

    // Load drafts from the server
    function loadDrafts() {
        fetch("/list_drafts/")
            .then((response) => response.json())
            .then((data) => {
                const draftsContainer = document.querySelector(".draft-group");
                draftsContainer.innerHTML = ""; // Clear existing drafts
                if (data.drafts) {
                    data.drafts.forEach((draft) => {
                        const button = document.createElement("button");
                        button.textContent = draft.name;
                        button.addEventListener("click", () => loadDraft(draft.id));
                        draftsContainer.appendChild(button);
                    });
                }
            });
    }

    // Load a specific draft
    function loadDraft(draftId) {
        selectedDraftId = draftId; // Set the selected draft ID
        fetch(`/load_draft/${draftId}/`)
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    const draft = data.draft;
                    document.getElementById("description").value = draft.description;
                    document.getElementById("audience").value = draft.audience;
                    document.getElementById("style").value = draft.style;
                    document.getElementById("tone").value = draft.tone;
                    document.getElementById("hashtags").value = draft.hashtags;

                    // If the field is saved as "Other," populate the textbox
                    if (draft.audience === "other") {
                        audienceTextBox.value = "";
                    }
                    if (draft.style === "other") {
                        styleTextBox.value = "";
                    }
                    if (draft.tone === "other") {
                        toneTextBox.value = "";
                    }

                    // Re-enable the textbox if "Other" is selected
                    toggleTextbox();
                } else {
                    alert("Failed to load draft.");
                }
            });
    }

    // Utility: Get CSRF Token
    function getCSRFToken() {
        return document.querySelector("[name=csrfmiddlewaretoken]").value;
    }

    // Load drafts on page load
    loadDrafts();
}});
