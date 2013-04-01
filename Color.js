function Color(r, g, b, a) {
	this.r = r;
	this.g = g;
	this.b = b;
	if(a === undefined) {
		a = 255;
	}
	this.a = a;
}

Color.prototype.toBackgroundColorString = function() {
	return "rgb(" + this.r + "," + this.g + "," + this.b + ")";
}

Color.prototype.diff = function(r, g, b) {
	var delta = Math.pow(this.r - r, 2);
	delta += Math.pow(this.g - g, 2);
	delta += Math.pow(this.b - b, 2);
	return Math.sqrt(delta);
}

Color.fromHexString = function(hexColorStr) {
	var r = parseInt(hexColorStr.substr(1,2), 16);
	var g = parseInt(hexColorStr.substr(3,2), 16);
	var b = parseInt(hexColorStr.substr(5,2), 16);
	return new Color(r, g, b);
}

Color.prototype.equals = function(c) {
	return this.r == c.r && this.g == c.g && this.b == c.b;
}