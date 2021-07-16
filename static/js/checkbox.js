var checkbox = document.getElementById('id_is_self_responsible');
var responsible_by = document.getElementById('id_responsible_by');

checkbox.addEventListener('change', function() {
    if (this.checked) {
        console.log("Checkbox is checked..");
        responsible_by.disabled = true;
    } else {
        console.log("Checkbox is not checked..");
        responsible_by.disabled = false;
    }
});