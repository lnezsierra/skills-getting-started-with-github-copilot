document.addEventListener("DOMContentLoaded", () => {
  // Cache the page elements shared by the signup and rendering flows.
  const activitiesList = document.getElementById("activities-list");
  const emailInput = document.getElementById("email");
  const messageDiv = document.getElementById("message");

  // Submit one student's email for the activity selected from its card.
  async function signupForActivity(activity, joinButton) {
    // Stop before making a request when the email field is invalid.
    if (!emailInput.reportValidity()) {
      emailInput.focus();
      return;
    }

    // Disable the button while the request is in progress.
    const originalButtonText = joinButton.textContent;
    joinButton.disabled = true;
    joinButton.textContent = "Joining...";

    try {
      // Send the activity and email to the signup endpoint.
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(emailInput.value)}`,
        { method: "POST" }
      );
      const result = await response.json();

      // Show the API result and refresh availability after a successful signup.
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
      // Handle network failures that do not return an API response.
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      console.error("Error signing up:", error);
    } finally {
      // Restore the button and briefly display the result message.
      joinButton.disabled = false;
      joinButton.textContent = originalButtonText;
      messageDiv.classList.remove("hidden");

      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    }
  }

  // Fetch the latest activity data and rebuild the activity cards.
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Remove the loading placeholder before inserting activity cards.
      activitiesList.innerHTML = "";

      Object.entries(activities).forEach(([name, details]) => {
        // Create the card shell for the current activity.
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        // Calculate capacity values used by the label and progress meter.
        const participantCount = details.participants.length;
        const spotsLeft = Math.max(details.max_participants - participantCount, 0);
        const capacityPercent = Math.min(
          Math.round((participantCount / details.max_participants) * 100),
          100
        );
        const availabilityClass = spotsLeft === 0 ? "full" : spotsLeft <= 3 ? "low" : "available";
        const availabilityText = spotsLeft === 0 ? "Activity full" : `${spotsLeft} spots left`;

        // Render the activity details and accessible capacity indicator.
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
          <div class="students-section">
            <h5>Registered Students</h5>
            <ul class="students-list"></ul>
          </div>
        `;

        // Insert participant emails as text to avoid interpreting user input as HTML.
        const studentsList = activityCard.querySelector(".students-list");
        const participantEmails = details.participants.length
          ? details.participants
          : ["No students registered yet"];

        participantEmails.forEach((studentEmail) => {
          const studentItem = document.createElement("li");
          studentItem.className = `student-chip${details.participants.length ? "" : " empty"}`;
          studentItem.textContent = studentEmail;
          studentsList.appendChild(studentItem);
        });

        // Add a card-specific signup button and disable it at capacity.
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

        // Insert the completed card into the activity list.
        activitiesList.appendChild(activityCard);
      });
    } catch (error) {
      // Replace the list with a useful message when activities cannot load.
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Load activities once the page and cached elements are ready.
  fetchActivities();
});
