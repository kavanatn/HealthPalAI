document.getElementById('health-form').addEventListener('submit', async function (event) {
  event.preventDefault(); // Prevent form submission until validation is done

  // Form validation
  let isValid = true;
  let errorMessage = "";

  // Collect form inputs
  const age = document.getElementById('age').value;
  const gender = document.getElementById('gender').value;
  const height = document.getElementById('height').value;
  const weight = document.getElementById('weight').value;
  const heartRate = document.getElementById('heart-rate').value;
  const sleep = document.getElementById('sleep').value;
  const physicalActivity = document.getElementById('physical-activity').value;
  const waterIntake = document.getElementById('water-intake').value;
  const diet = Array.from(document.querySelectorAll('input[name="diet"]:checked'))
                    .map(input => input.value); // Get selected checkboxes for diet preferences
  const chronicConditions = document.getElementById('chronic-conditions').value;
  const allergies = document.getElementById('allergies').value;
  const smoking = document.getElementById('smoking').value;
  const alcohol = document.getElementById('alcohol').value;

  // Validate form fields
  if (isNaN(age) || age < 1 || age > 120) {
    isValid = false;
    errorMessage += "Please enter a valid age (1-120).\n";
  }

  if (isNaN(height) || height < 50 || height > 250) {
    isValid = false;
    errorMessage += "Please enter a valid height (between 50 cm and 250 cm).\n";
  }

  if (isNaN(weight) || weight < 0 || weight > 500) {
    isValid = false;
    errorMessage += "Please enter a valid weight (between 0 kg and 500 kg).\n";
  }

  if (isNaN(heartRate) || heartRate < 30 || heartRate > 200) {
    isValid = false;
    errorMessage += "Please enter a valid heart rate (between 30 bpm and 200 bpm).\n";
  }

  if (isNaN(sleep) || sleep < 0 || sleep > 20) {
    isValid = false;
    errorMessage += "Please enter valid sleep hours (between 0 and 20 hours).\n";
  }

  if (isNaN(waterIntake) || waterIntake < 0.5 || waterIntake > 10) {
    isValid = false;
    errorMessage += "Please enter a valid water intake (between 0.5 liters and 10 liters).\n";
  }

  if (diet.length === 0) {
    isValid = false;
    errorMessage += "Please select at least one diet preference.\n";
  }

  // If the form is invalid, show an alert with all errors
  if (!isValid) {
    alert(errorMessage);
    return; // Prevent form submission if validation fails
  }

  // Prepare form data for submission
  const formData = new FormData();
  formData.append("age", age);
  formData.append("gender", gender);
  formData.append("height", height);
  formData.append("weight", weight);
  formData.append("heart-rate", heartRate);
  formData.append("sleep", sleep);
  formData.append("physical-activity", physicalActivity);
  formData.append("water-intake", waterIntake);
  diet.forEach(d => formData.append('diet', d));
  formData.append("chronic-conditions", chronicConditions);
  formData.append("allergies", allergies);
  formData.append("smoking", smoking);
  formData.append("alcohol", alcohol);

  // Show loading overlay before sending the data
  let overlay = document.getElementById("loading-overlay");
  overlay.style.display = "flex";

  try {
    // Send the form data via a POST request
    const response = await fetch('http://localhost:5000/submit', {
      method: 'POST',
      body: formData
    });

    // Parse the response as HTML (assuming Flask will render the template)
    const text = await response.text();

    // Assuming you will receive a full HTML page (the 'dashboard.html' page)
    // Display the recommendations dynamically
    document.querySelector('.recommendations').innerHTML = text;

  } catch (error) {
    console.error('Error fetching recommendations:', error);
    alert('Failed to generate recommendations. Please try again.');
  } finally {
    // Hide the loading overlay after submission attempt
    overlay.style.display = "none";
  }
}); 
