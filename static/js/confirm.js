$(function myFunction()
{
var x;
var r=confirm("Are you ready to add?");
if (r==true)
  {
  	x="Let's do this!";
  }
else
  {
  	x="Okay, see ya!";
  }
document.getElementById("confirm").innerHTML=x;
});
