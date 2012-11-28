function easterEgg() {
	var soundfile = "/media/audio/stopit" + Math.floor(1 + Math.random() * 3)
		+ ".mp3";
	document.getElementById("dummy").innerHTML = "<audio id='audioEasterEgg' src=" + "'" + soundfile + "'" + 
		" />";
		document.getElementById('audioEasterEgg').play();
}