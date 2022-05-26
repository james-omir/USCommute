function switchPage(){
	var state = document.getElementById("selector");
	var picked = state.options[state.selectedIndex].value;
	window.location.replace(picked);
}
