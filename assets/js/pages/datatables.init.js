/******/ (function() { // webpackBootstrap
var __webpack_exports__ = {};
/*!***********************************************!*\
  !*** ./resources/js/pages/datatables.init.js ***!
  \***********************************************/
$(document).ready(function () {
  $("#datatable").DataTable(), $("#datatable-buttons").DataTable({
    lengthChange: !1,
    buttons: ["copy", "excel", "pdf", "colvis"]
  }).buttons().container().appendTo("#datatable-buttons_wrapper .col-md-6:eq(0)"), $(".dataTables_length select").addClass("form-select form-select-sm");


//   $('#mytable').DataTable({
//     "paging": false,
//     "ordering": false,
//     "info": false,
//     "bFilter": true,
//     "pageLength": 100,
//     "dom": "lrtip"
// });

// $('#myCustomSearchBox').keyup(function() {
//     dTable.search($(this).val()).draw(); // this  is for customized searchbox with datatable search feature.
// });
});
/******/ })()
;