// when the page loads
window.onload = function () {
  addClassesToTables();
}

function addClassesToTables() {
  // get all tables in window
  var tables = document.getElementsByTagName("table"),
    len_tables = tables !== null ? tables.length : 0,
    i = 0;
  // loop through each table
  for (i; i < len_tables; i++) {
    // add classes to each table
    tables[i].className += " table table-sm table-borderless text-center";

    // get all the cells in each table
    var cells = document.getElementsByTagName("td"),
      len_cells = cells !== null ? cells.length : 0,
      j = 0;
    // loop through each cell
    for (j; j < len_cells; j++) {
      // add classes to cell
      cells[j].className += " align-middle";
    }
  }
}