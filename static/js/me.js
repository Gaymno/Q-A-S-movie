window.onload=function(){
	var btn_1=document.getElementById("btn_1");
	var btn_2=document.getElementById("btn_2");
	var close=document.getElementsByClassName("close");
	var close_1=document.getElementsByClassName("close_1");
	var dialog=document.getElementsByClassName("dialog");
	var form_1=document.getElementsByClassName("form_1");
	var form_2=document.getElementsByClassName("form_2");
	btn_1.addEventListener('click',function(){
		form_1[0].className="form_1 open";
	})
	btn_2.addEventListener('click',function(){
		form_2[0].className="form_2 open";
	})
	close[0].addEventListener('click',function(){
		form_1[0].className="form_1";
	})
	// btn_2.addEventListener('click',function(){
	// 	dialog[0].style.visibility='visible';
	// })
	close_1[0].addEventListener('click',function(){
		form_2[0].className="form_2";
	})	
}
