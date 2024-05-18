function toggleCheckboxes(clickedCheckbox) {
    const checkboxes = document.querySelectorAll('.sort_checkbox');
    checkboxes.forEach(checkbox => {
        if (checkbox !== clickedCheckbox) {
            checkbox.checked = false;
        }
    });
}