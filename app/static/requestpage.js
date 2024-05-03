document.getElementById("submited").addEventListener("click", function() {
    alert("Hello World!");
  });


// Get references to the dropdowns
const firstDropdown = document.getElementById('firstDropdown');
const secondDropdown = document.getElementById('secondDropdown');

const csranks=['SILVER','GOLD NOVA','MASTER GUARDIAN','LEGENDARY']
const owranks=['BRONZE','SILVER','GOLD','PLATNIUM','DIAMOND','MASTER','GRANDMASTER','CHAMPIONS','TOP500']
const leagueranks=['IRON','BRONZE','SILVER','GOLD','PLATINUM','EMERALD','DIAMOND','MASTER','GRANDMASTER','CHALLENGER']
const valranks=['IRON','BRONZE','SILVER','GOLD','PLATINUM','DIAMOND','ASCENDANT','IMMORTAL','RADIANT']
const gamesapp={
    'CSGO':csranks,'Overwatch':owranks,'League':leagueranks,'Valorant':valranks};
// Define options for the second dropdown based on the selection in the first dropdown
const optionsByCategory = {
  '1': ['Option 1.1', 'Option 1.2', 'Option 1.3'],
  '2': ['Option 2.1', 'Option 2.2', 'Option 2.3']
};

// Function to update options of the second dropdown based on the selection in the first dropdown
function updateSecondDropdown() {
  const category = firstDropdown.value;
  // Clear existing options
  secondDropdown.innerHTML = '<option value="">Select an option</option>';
  // Add options based on the selected category
  gamesapp[category].forEach(option => {
    const optionElement = document.createElement('option');
    optionElement.textContent = option;
    optionElement.value = option;
    secondDropdown.appendChild(optionElement);
  });
  // Show the second dropdown
  secondDropdown.style.display = 'inline';
}

// Event listener to trigger update of the second dropdown when the first dropdown selection changes
firstDropdown.addEventListener('change', updateSecondDropdown);
