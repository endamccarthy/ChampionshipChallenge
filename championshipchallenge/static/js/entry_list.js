var tableRows = document.getElementsByClassName("clickable-row");

for (let row of tableRows) {
  row.addEventListener('click', function () {
    window.location = row.attributes.getNamedItem("data-href").value;
  });
}