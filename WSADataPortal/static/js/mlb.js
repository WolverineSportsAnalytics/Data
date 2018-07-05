function displayTable(){
	var sel1 = document.querySelector('#sel1');
	var sel2 = document.querySelector('#sel2');
	console.log(sel1.value + "/" + sel2.value);
	tables = document.getElementsByClassName("myTable");
	var i;
	for (i = 0; i < tables.length; i++) {
	  tables[i].style.display = "none";
	}
	table = document.getElementById(sel1.value + "/" + sel2.value)
	table.style.display = "table";
}

window.onload = function() {
	displayTable();
};
