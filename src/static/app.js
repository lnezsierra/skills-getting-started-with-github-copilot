document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");
  const activityPlaceholder = '<option value="">-- Select an activity --</option>';

  function createDetailRow(label, value) {
    const row = document.createElement("p");
    const strong = document.createElement("strong");

    strong.textContent = `${label}: `;
    row.appendChild(strong);
    row.append(value);

    return row;
  }

  function createParticipantSection(participants) {
    const section = document.createElement("div");
    section.className = "participants-section";

    const header = document.createElement("div");
    header.className = "participants-header";

    const title = document.createElement("h5");
    title.textContent = "Participants";

    const count = document.createElement("span");
    count.className = "participants-count";
    count.textContent = `${participants.length} enrolled`;

    header.append(title, count);
    section.appendChild(header);

    if (participants.length === 0) {
      const emptyState = document.createElement("p");
      emptyState.className = "participants-empty";
      emptyState.textContent = "No one has signed up yet.";
      section.appendChild(emptyState);
      return section;
    }

    const list = document.createElement("ul");
    list.className = "participants-list";

    participants.forEach((participant) => {
      const item = document.createElement("li");
      item.textContent = participant;
      list.appendChild(item);
    });

    section.appendChild(list);
    return section;
  }

  function createActivityCard(name, details) {
    const activityCard = document.createElement("div");
    activityCard.className = "activity-card";

    const spotsLeft = details.max_participants - details.participants.length;
    const title = document.createElement("h4");
    const description = document.createElement("p");

    title.textContent = name;
    description.className = "activity-description";
    description.textContent = details.description;

    activityCard.append(
      title,
      description,
      createDetailRow("Schedule", details.schedule),
      createDetailRow("Availability", `${spotsLeft} spots left`),
      createParticipantSection(details.participants)
    );

    return activityCard;
  }

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Reset rendered content before repopulating from the API.
      activitiesList.innerHTML = "";
      activitySelect.innerHTML = activityPlaceholder;

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = createActivityCard(name, details);

        activitiesList.appendChild(activityCard);

        // Add option to select dropdown
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

  // Handle form submission
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
        messageDiv.textContent = result.message;
        messageDiv.className = "message success";
        signupForm.reset();
        await fetchActivities();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "message error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "message error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();
});
