function dropDown() {
    document.getElementById('dropdown-menu-id').classList.toggle('show')
}

function dropBurger() {
    document.getElementById('burger-menu-id').classList.toggle('show')
    document.getElementById('burger').classList.toggle('open')
}

window.onclick = function(event) {
    if (document.getElementById('dropdown-menu-id').classList.contains('show')) {
        if (!document.getElementById('dropdown-button-id').contains(event.target) &&
        !document.getElementById('dropdown-menu-id').contains(event.target)) {
            document.getElementById('dropdown-menu-id').classList.remove('show')
            
        } 
    } else if (document.getElementById('burger-menu-id').classList.contains('show')) {
        if(!document.getElementById('burger-menu-id').contains(event.target) &&
        !document.getElementById('burger').contains(event.target)) {
            document.getElementById('burger-menu-id').classList.remove('show')
            document.getElementById('burger').classList.remove('open')
        }
    }  
}