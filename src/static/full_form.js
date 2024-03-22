// PDF FILE
let fileInput = document.querySelector('input#file');
fileInput.addEventListener('change', () => {
    if(!fileInput.files[0].type.match('.*pdf$')) {
        fileInput.value = '';
        alert('התוכנה עובדת עם קבצי PDF בלבד!');
    }
});

// SAVE FOR OTHERS TRIGGER
let sfo_inputs = document.querySelectorAll('#sfo-form input, #sfo-form select');
function disable_sfo() {
    sfo_inputs.forEach(input => input.setAttribute('disabled', true));
}
function enable_sfo() {
    sfo_inputs.forEach(input => input.removeAttribute('disabled'));
}
disable_sfo();

let sfo_check = document.getElementById('sfo-check');
sfo_check.addEventListener('change', event => {
    if(sfo_check.checked)
        enable_sfo();
    else {
        disable_sfo();
    }
});

// ADVANCED SETTINGS CARD TRIGGER
let adv_set_card = document.querySelector('#adv_set_card');
function disable_adv_set() {
    adv_set_card.classList.add('hide');
}
function enable_adv_set() {
    adv_set_card.classList.remove('hide');
}
disable_adv_set();

let adv_set_check = document.getElementById('adv-set-check');
adv_set_check.addEventListener('change', event => {
    if(adv_set_check.checked)
        enable_adv_set();
    else {
        disable_adv_set();
    }
});

// let form = document.querySelector('form');
// form.addEventListener('submit', () => {
//     alert(form.getAttribute('aria-onsubmit-text'));
//     window.open(form.getAttribute('aria-created-url'));
// });

// MULTIPLE SELECT
function updateCheckbox(select, input, label) {
    let str = '';
    let labelStr = '';
    select.querySelectorAll('input[type="checkbox"]').forEach(option => {
        if (option.checked) {
            str += option.value + '-';
            labelStr += option.value + ' ';
        }
    });
    input.value = str.substring(0, str.length-1);
    
    if(input.value.length == "") {
        label.innerText = label.getAttribute('aria-default-text');
    } else {
        label.innerText = labelStr;
    }
}


let genreSelect = document.getElementById('sfo-genre-select');
let genreLabel = genreSelect.querySelector('#sfo-anchor');
let genreInput = document.getElementById('sfo-genre-input');
let genreUpdateCheckbox = () => updateCheckbox(genreSelect, genreInput, genreLabel);

genreSelect.querySelectorAll('input[type="checkbox"]').forEach(option => {
    option.addEventListener('change', genreUpdateCheckbox);
});

let checkList = document.getElementById('sfo-genre-select');
checkList.getElementsByClassName('anchor')[0].onclick = function(evt) {
  if (checkList.classList.contains('visible'))
    checkList.classList.remove('visible');
  else if(sfo_check.checked)
    checkList.classList.add('visible');
}
