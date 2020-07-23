// when the page loads
window.onload = function () {
  addClassesToTables();
}

function addClassesToTables() {
  // get all tables in window
  var tables = document.getElementsByTagName("table");
  // loop through each table
  for (let table of tables) {
    table.className += " table table-sm table-borderless text-center";
    // get all the cells in each table
    var cells = document.getElementsByTagName("td");
    // loop through each cell
    for (let cell of cells) {
      cell.className += " align-middle";
    }
  }
}