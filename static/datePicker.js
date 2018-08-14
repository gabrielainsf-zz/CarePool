// Datepicker
// $( function() {
//   $( "#datepicker" ).datepicker();
// } );

// var datepicker = $.fn.datepicker.noConflict();
$.noConflict();
jQuery( document ).ready(function( $ ) {
    $(function() {
    $( "#datepicker" ).datepicker('option', 'dateFormat', 'yy-mm-dd');
    } );
});