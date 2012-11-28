function easterEgg() {
	var soundfile = "/media/audio/stopit" + Math.floor(1 + Math.random() * 3)
		+ ".wav";
	var innerHTML = 		
		"<embed src=" + "'" + soundfile + "'" + 
		" hidden='true' autostart='true' loop='false' />";
	document.getElementById("dummy").innerHTML = innerHTML;

}