const hazardCheckboxes = document.querySelectorAll('input[name="hazard"]');
const alertButton = document.getElementById("checkAlert");
const alertContent = document.getElementById("alertContent");

// Ensure only one checkbox can be selected at a time
hazardCheckboxes.forEach(checkbox => {
    checkbox.addEventListener('change', () => {
        if (checkbox.checked) {
            hazardCheckboxes.forEach(cb => {
                if (cb !== checkbox) cb.checked = false;
            });
        }
    });
});

alertButton.addEventListener("click", async () => {
    const selectedHazard = Array.from(hazardCheckboxes).find(cb => cb.checked)?.value;
    if (!selectedHazard) {
        alertContent.textContent = "Please select a hazard type.";
        return;
    }

    alertContent.textContent = "Fetching alerts...";

    try {
        const { data, error } = await supabase
            .from("alerts")
            .select("*")
            .eq("alertType", selectedHazard)
            .eq("region", "jackson")
            .order("alertDate", { ascending: false })
            .limit(5);

        if (error) {
            alertContent.textContent = "Error fetching alerts.";
            console.error(error);
        } else if (!data || data.length === 0) {
            alertContent.textContent = "No current alerts.";
        } else {
            alertContent.innerHTML = data.map(a => `
                <strong>${a.alertType.toUpperCase()} - ${a.alertLevel}</strong><br>
                ${a.actionTaken || "No action yet."}<br>
                <em>${new Date(a.alertDate).toLocaleString()}</em><br><hr>
            `).join('');
        }
    } catch (err) {
        alertContent.textContent = "Unexpected error occurred.";
        console.error(err);
    }
});

document.getElementById("checkAlert").addEventListener("click", () => {
  const hazard = document.querySelector('input[name="hazard"]:checked')?.value;
  if (!hazard) return alert("Please select Flood or Air Quality.");

  let alertMessage = "";
  if (hazard === "flood") {
    const waterDirty = Math.floor(Math.random() * 101);
    alertMessage =
      waterDirty > 70
        ? ` Dirty water level ${waterDirty}% detected. Boil water.`
        : " Water quality looks safe.";
  } else if (hazard === "air") {
    const aqi = Math.floor(Math.random() * 201);
    alertMessage =
      aqi > 100
        ? ` AQI is ${aqi}. Stay indoors and limit outdoor activities.`
        : "Air quality is good.";
  }

  document.getElementById("alertContent").innerText = alertMessage;
});