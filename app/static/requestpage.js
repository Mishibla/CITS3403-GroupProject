$(document).ready(function() {
  //linking the games dropdown with its corresponding rank
  const firstDropdown = $('#games');
  const secondDropdown = $('#ranks');
  const csranks=['SILVER','GOLD NOVA','MASTER GUARDIAN','LEGENDARY']
  const owranks=['BRONZE','SILVER','GOLD','PLATNIUM','DIAMOND','MASTER','GRANDMASTER','CHAMPIONS','TOP500']
  const leagueranks=['IRON','BRONZE','SILVER','GOLD','PLATINUM','EMERALD','DIAMOND','MASTER','GRANDMASTER','CHALLENGER']
  const valranks=['IRON','BRONZE','SILVER','GOLD','PLATINUM','DIAMOND','ASCENDANT','IMMORTAL','RADIANT']
  const gamesapp={
      'CSGO':csranks,'Overwatch':owranks,'League':leagueranks,'Valorant':valranks};
  //linking skins with exclusive skins
  const skin = $("#skins");
  const exclusivity = $('#exclusive');
  const label_exclu = $('#exclusive_label')
  
  function updateSecondDropdown() {
    const category = firstDropdown.val();
    // Clear existing options
    secondDropdown.html('<option value="">Select an option</option>');
    // Add options based on the selected category
    gamesapp[category].forEach(option => {
      const optionElement = $('<option>').text(option).val(option);
      secondDropdown.append(optionElement);
    });
    // Show the second dropdown
    secondDropdown.css('display', 'inline');
  }
  //function to handle the exclusive checkbox
  function exclusives() {
    if (skin.val() === 'True') {
      label_exclu.show();
      exclusivity.show();
    } else {
      exclusivity.hide();
      label_exclu.hide();
    }
  }
  // Event listener to trigger update of the second dropdown when the first dropdown selection changes
  firstDropdown.change(updateSecondDropdown);
  skin.change(exclusives);
  //only allows max 4 images
  $('#images').on('change', function(event) {
    const selectedFilesCount = $(this)[0].files.length;
    if (selectedFilesCount > 4) {
      alert('You can only select up to 4 files.');
      $(this).val(null); // Clear the file input
    }
  })
  $(document).ready(function() {
    var unsuccessfulSubmit = $('body').data('unsuccessful');
    if (unsuccessfulSubmit) {
      $('#ranks').show();
      $('#exclusive').show();
      $('#exclusive_label').show();
    }
  });
  
});
