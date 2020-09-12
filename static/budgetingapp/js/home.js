
function hideCard(idText) { 
  document.getElementById(idText).style.display="none"; 
}

// TODO: Put this in a function?
$(document).ready(function(){
  var now = new Date();
  var hrs = now.getHours();
  var msg = "";
  if (hrs < 12 && hrs >=  0){
    msg = ("Good Morning!");
  } else if (hrs < 17){
    msg = ("Good afternoon");
  } else {
    msg = ("Good evening");
  }
  document.getElementById('goodTimeText').innerHTML = msg;
});
/* 
*/



