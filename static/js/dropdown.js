function dropDown() {
    document.getElementById('dropdown-menu-id').classList.toggle('show')
}

window.onclick = function(event) {
    if (document.getElementById('dropdown-button-id').contains(event.target)) {
        console.log('clicked inside')
    } else {
        document.getElementById('dropdown-menu-id').classList.remove('show')
    }
}