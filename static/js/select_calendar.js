const selectСalendar = document.getElementById('select_calendar');

function changeOption(){
    const selectedOption = selectСalendar.options[selectСalendar.selectedIndex];
    window.location.replace('/calendar/' + selectedOption.value);
}

selectСalendar.addEventListener("change", changeOption);
