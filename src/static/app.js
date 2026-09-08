document.addEventListener("DOMContentLoaded", () => {
  // Cache DOM references used throughout the app.
  const activitiesList = document.getElementById("activities-list");
  const emailInput = document.getElementById("email");
  const messageDiv = document.getElementById("message");

  async function signupForActivity(activity, joinButton) {
    if (!emailInput.reportValidity()) {
      emailInput.focus();
      return;
    }

    const originalButtonText = joinButton.textContent;
    joinButton.disabled = true;
    joinButton.textContent = "Joining...";

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(emailInput.value)}`,
        { method: "POST" }
      );
      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        emailInput.value = "";
        await fetchActivities();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      console.error("Error signing up:", error);
    } finally {
      joinButton.disabled = false;
      joinButton.textContent = originalButtonText;
      messageDiv.classList.remove("hidden");

      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    }
  }

  // Fetch activities from the backend and render cards.
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message
      activitiesList.innerHTML = "";

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

        const joinButton = document.createElement("button");
        joinButton.type = "button";
        joinButton.className = "activity-join-button";
        joinButton.disabled = spotsLeft === 0;
        joinButton.textContent = spotsLeft === 0 ? "Activity full" : "Join activity";
        joinButton.setAttribute("aria-label", `${joinButton.textContent}: ${name}`);
        joinButton.addEventListener("click", () => {
          signupForActivity(name, joinButton);
        });
        activityCard.appendChild(joinButton);

        activitiesList.appendChild(activityCard);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Initial data load when the page is ready.
  fetchActivities();
});
