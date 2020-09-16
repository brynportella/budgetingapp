function hideCard(idText) { 
  document.getElementById(idText).style.display="none"; 
}

/* JQuery
*/
$(function () {
  $("#id_goal_date").datetimepicker({
    format: 'd/m/Y H:i',
  });
});



