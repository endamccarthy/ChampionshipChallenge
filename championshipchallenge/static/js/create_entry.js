const form = document.querySelector('#form'),
  confirmSubmitForm = document.querySelector('#confirmSubmitForm');

confirmSubmitForm.addEventListener('click', function () {
  form.submit();
});