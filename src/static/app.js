document.addEventListener("DOMContentLoaded", () => {
  // Cache DOM references used throughout the app.
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // Fetch activities from the backend and render cards + select options.
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message
      activitiesList.innerHTML = "";
      activitySelect.length = 1;

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        // Compute remaining seats based on current participants.
        const participantCount = details.participants.length;
        const spotsLeft = Math.max(details.max_participants - participantCount, 0);
        const capacityPercent = Math.min(
          Math.round((participantCount / details.max_participants) * 100),
          100
        );
        const availabilityClass = spotsLeft === 0 ? "full" : spotsLeft <= 3 ? "low" : "available";
        const availabilityText = spotsLeft === 0 ? "Activity full" : `${spotsLeft} spots left`;

        activityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <div class="availability ${availabilityClass}">
            <div class="availability-summary">
              <strong>Availability</strong>
              <span>${availabilityText}</span>
            </div>
            <div
              class="capacity-meter"
              role="progressbar"
              aria-label="${name} capacity"
              aria-valuemin="0"
              aria-valuemax="${details.max_participants}"
              aria-valuenow="${participantCount}"
              aria-valuetext="${participantCount} of ${details.max_participants} spots filled"
            >
              <span class="capacity-meter-fill" style="width: ${capacityPercent}%"></span>
            </div>
            <small>${participantCount} of ${details.max_participants} spots filled</small>
          </div>
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

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

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
        signupForm.reset();
        await fetchActivities();
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

  // Initial data load when the page is ready.
  fetchActivities();
});
