const form = document.getElementById('form'),
  confirmSubmitForm = document.getElementById('confirmSubmitForm');

confirmSubmitForm.addEventListener('click', function () {
  form.submit();
});