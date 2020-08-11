// get elements from DOM
const form = document.getElementById('form'),
  confirmSubmitForm = document.getElementById('confirmSubmitForm'),
  submitButton = document.getElementById('submitButton'),
  fields = form.querySelectorAll("[required]");

// event listeners
form.addEventListener('change', checkIfFormIsFilled);
confirmSubmitForm.addEventListener('click', submitForm);

// check to see if form is filled up before enabling submit button
function checkIfFormIsFilled() {
  for (let i = 0; i < fields.length; i++) {
    if (!fields[i].checkValidity()) {
      submitButton.disabled = true;
      break;
    }
    submitButton.disabled = false;
  }
}

function submitForm() {
  form.submit();
}