document.addEventListener("DOMContentLoaded", () => {
  const REQUIRED_EMAIL_DOMAIN = "@merginton.edu";

  // Cache DOM references used throughout the app.
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");
  const participantsList = document.getElementById("participants-list");
  const participantsEmpty = document.getElementById("participants-empty");

  function getEmailLocalPart(email) {
    return email.split("@")[0];
  }

  function renderParticipants(participants) {
    participantsList.innerHTML = "";

    if (!participants.length) {
      participantsList.classList.add("hidden");
      participantsEmpty.textContent = "No students are registered for this activity yet.";
      participantsEmpty.classList.remove("hidden");
      return;
    }

    participants.forEach((email) => {
      const participantItem = document.createElement("li");
      participantItem.textContent = getEmailLocalPart(email);
      participantsList.appendChild(participantItem);
    });

    participantsEmpty.classList.add("hidden");
    participantsList.classList.remove("hidden");
  }

  async function fetchActivityParticipants(activityName) {
    if (!activityName) {
      participantsList.classList.add("hidden");
      participantsList.innerHTML = "";
      participantsEmpty.textContent = "Select an activity to view registered students.";
      participantsEmpty.classList.remove("hidden");
      return;
    }

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activityName)}/participants`
      );
      const result = await response.json();

      if (!response.ok) {
        participantsList.classList.add("hidden");
        participantsList.innerHTML = "";
        participantsEmpty.textContent = result.detail || "Unable to load registered students.";
        participantsEmpty.classList.remove("hidden");
        return;
      }

      renderParticipants(result.participants || []);
    } catch (error) {
      participantsList.classList.add("hidden");
      participantsList.innerHTML = "";
      participantsEmpty.textContent = "Failed to load registered students.";
      participantsEmpty.classList.remove("hidden");
      console.error("Error fetching participants:", error);
    }
  }

  // Fetch activities from the backend and render cards + select options.
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message
      activitiesList.innerHTML = "";
      activitySelect.innerHTML = '<option value="">-- Select an activity --</option>';

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        // Compute remaining seats based on current participants.
        const spotsLeft = details.max_participants - details.participants.length;

        activityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
        `;

        activitiesList.appendChild(activityCard);

        // Keep the signup dropdown synchronized with visible activities.
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Submit signup requests to the API and display server feedback.
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value.trim().toLowerCase();
    const activity = document.getElementById("activity").value;

    if (!email.endsWith(REQUIRED_EMAIL_DOMAIN)) {
      messageDiv.textContent = `Email must use the ${REQUIRED_EMAIL_DOMAIN} domain`;
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      return;
    }

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        // Success path: show confirmation and clear form.
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        await fetchActivityParticipants(activity);
        signupForm.reset();
      } else {
        // Error path: prefer API detail when available.
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      // Network or unexpected runtime errors.
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  activitySelect.addEventListener("change", (event) => {
    fetchActivityParticipants(event.target.value);
  });

  // Initial data load when the page is ready.
  fetchActivities();
});






