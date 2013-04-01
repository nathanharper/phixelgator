#!/usr/bin/env python
import os, sys, argparse

def phixelate(input, palette):
  print("hey")
  return "hey"

if __name__=="__main__":
  parse = argparse.ArgumentParser( \
      description="Create \"pixel art\" from a photo", \
      prog='phixel', \
      epilog="Disclaimer: this does not \"really\" make pixel art, it just \
        reduces the image resolution with preset color palettes.")
  parse.add_argument('-p', '--palette', \
      choices=['all','mario','flash','zelda','kungfu','tetris','contra'], default='all', \
      help="The color palette to use")
  parse.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin, \
      help="the input file (defaults to stdin)")
  parse.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout, \
      help="the output file (defaults to stdout)")
  args = parse.parse_args()

  try:
    phixel = phixelate(args.infile.read(), args.palette)
  except Error:
    print("something bad happened")
    args.infile.close()
    args.outfile.close()
    sys.exit(1)

  args.infile.close()
  args.outfile.write(phixel)
  args.outfile.close()
  sys.exit(0)

# var canvas = null;
# var originalImage = null;
# var blockSize = null;

# var file = null;
# var fileReader = null;

# var selectedPalette = null;
# var usePreset = true;
# var presetPalettes = [];
# var presetMore = false;

# var processedNumBlocks = 0;
# var totalNumBlocks = 0;
# var renderInProgress = false;

# var shareLink = null;
# var shareFunc = null;

# var useFile = false;
# var useURL = false;

# var embedLogo;

# //entry point
# $(document).ready(function() {
# 	/*
# 	var is_chrome = navigator.userAgent.toLowerCase().indexOf('chrome') > -1;
# 	if(!is_chrome) {
# 		alert("Please use Google Chrome for best results");
# 	}
# 	*/
	
# 	embedLogo = new Image();
# 	embedLogo.src = "img/spt_logo_150x150.png";
	
# 	$("#blockSizeInput").val("8");
	
# 	$("#fileInput").change(function(event) {
# 		blockSize = null;
# 		file = event.currentTarget.files[0];
		
# 		//preset the filename
# 		$("#filename").val(file.name);
			
# 		//preset the type if possible
# 		var idx = file.name.lastIndexOf(".");
# 		if(idx != -1) {
# 			var fileExt = file.name.substring(idx+1, file.name.length);
# 			if(fileExt.toUpperCase() == "png") {
# 				//todo
# 			}
# 		}
		
# 		updateFilename();
# 		fileReader = new FileReader();
# 		fileReader.onload = fileLoadHandler;
# 		fileReader.readAsDataURL(file);
# 	});
	
# 	$("input[name=filetype]").change(updateFilename);
# 	$("#url_input").change(function() {
# 		useFile = false;
# 	});
	
# 	//handler for upload button
# 	$("#upload").click(function() {
# 		if(useFile) {
# 			setImage(img);
# 		}
# 		else {
# 			urlLoadHandler();
# 		}
# 	});
	
# 	//handler for render button
# 	$("#generateButton").click(function() {
# 		if(renderInProgress) {
# 			renderInProgress = false;
# 			$("#generateButton").html("RENDER");
# 		}
# 		else {
# 			$("#generateButton").html("STOP");
# 			renderInProgress = true;
# 			if(canvas == null) {
# 				alert("please select a file first");
# 				return;
# 			}
# 			try {
# 				blockSize = parseInt($("#blockSizeInput").val());
# 			}
# 			catch(err) {
# 				alert("please enter a valid block size");
# 			}
# 			setImage(originalImage);
# 			processCanvas(canvas[0], blockSize);
# 		}		
# 	});
	
# 	//handler for save button
# 	$("#saveImageButton").click(function() {
# 		var width = parseInt($("#save_width").val());
# 		var height  = parseInt($("#save_height").val());
# 		var filename = $("#filename").val();
# 		if($("#png")[0].checked) {
# 			Canvas2Image.saveAsPNG(canvas[0], false, width, height, filename);
# 		}
# 		else if($("#jpg")[0].checked) {
# 			Canvas2Image.saveAsJPEG(canvas[0], false, width, height, filename);
# 		}
# 		else {
# 			Canvas2Image.saveAsBMP(canvas[0], false, width, height, filename);
# 		}
# 	});
	
# 	$("#save_width").change(function() {
# 		if($("#lock_ratio").attr("checked") != null) {
# 			adjustHeight();
# 		}
# 	});
# 	$("#save_height").change(function() {
# 		if($("#lock_ratio").attr("checked") != null) {
# 			adjustWidth();
# 		}
# 	});
	
# 	//handler for fit to screen checkbox	
# 	$("#fit_to_screen").change(function() {
# 		fitToScreen();
# 	});
	
# 	//handler for zoom
# 	$("#zoom_range").change(function() {
# 		setCanvasZoom();
# 	});
	
# 	//handler for creates palette button
# 	$("#create_palette").click(function() {
# 		var newPalette = CustomPalette.addNewPalette();
# 		addPalette(newPalette, true);
# 	});
	
# 	CustomPalette.load();
# 	var i;
# 	for(i = 0; i < CustomPalette.myPalettes.length; i++) {
# 		var palette = CustomPalette.myPalettes[i];
# 		addPalette(palette);
# 	}
	
# 	presetPalettes.push(loadPresetPalette(SUPERMARIOBROS_PALETTE));	
# 	presetPalettes.push(loadPresetPalette(FLASHMAN_PALETTE));
# 	presetPalettes.push(loadPresetPalette(HYRULE_PALETTE));
# 	presetPalettes.push(loadPresetPalette(KUNGFU_PALETTE));
# 	presetPalettes.push(loadPresetPalette(TETRIS_PALETTE));
# 	presetPalettes.push(loadPresetPalette(CONTRA_PALETTE));	
# 	presetPalettes.push(loadPresetPalette(GRAYSCALE_PALETTE));
# 	presetPalettes.push(loadPresetPalette(NES_PALETTE));
# 	presetPalettes.push(loadPresetPalette(APPLE_II_PALETTE));
# 	presetPalettes.push(loadPresetPalette(GAMEBOY_PALETTE));
# 	presetPalettes.push(loadPresetPalette(COMMODORE64_PALETTE));
# 	presetPalettes.push(loadPresetPalette(INTELLIVISION_PALETTE));
# 	presetPalettes.push(loadPresetPalette(SEGA_MASTER_SYSTEM_PALETTE));
# 	presetPalettes.push(loadPresetPalette(ATARI2600_PALETTE));
	
# 	$("input[name=colorpalette]").change(function(ev) {
# 		if(selectedPalette != null && selectedPalette.isCustom) {
# 			$("#" + selectedPalette.name).removeClass("selected");
# 		}
# 		var idx = parseInt(ev.currentTarget.id);
# 		if(idx == -1) {
# 			selectedPalette = null;
# 		}
# 		else {
# 			selectedPalette = presetPalettes[idx];
# 		}
# 	});
	
# 	//handler for clicking on the preset pelette
# 	$("#preset_palettes").click(function() {
# 		usePreset = true;
# 	});
	
# 	//handler for clicking on the custom pelette
# 	$("#custom_palettes").click(function() {
# 		usePreset = false;
# 	});
	
# 	//handler for click on more/less button for preset palettes
# 	$("#more-less").click(function() {
# 		if(presetMore) {
# 			$(this).html("more");
# 		}
# 		else {
# 			$(this).html("less");
# 		}
# 		$("#more-less-btns").toggleClass("show");
# 	});
	
# 	$("#addcolorbutton").click(function() {
# 		if(!usePreset && selectedPalette != null && selectedPalette.isCustom) {
# 			var color = Color.fromHexString($("#colorpicker").val());
# 			if(selectedPalette.addColor(color)) {
# 				var colorElem = createColorElem(selectedPalette, color);
# 				$("#" + selectedPalette.name + " .custom_palette_colors").append(colorElem);
# 			}
# 			else {
# 				alert("Please add a unique color to this palette");
# 			}
# 		}
# 		else {
# 			alert("Please select a custom palette first");
# 		}
# 	});
	
# 	//embed logo
# 	$("#remove_logo").change(function() {
# 		if($("#remove_logo").attr("checked") != null) {
# 			console.log("Please support the development of Super Pixel Time by donating");
# 		}
# 	});
	
# 	//sharing 
# 	$("#generate_link").click(function() {
# 		$.post("upload_file.php", {
# 			data: canvas[0].toDataURL()
# 		}, function(filename) {
# 			shareLink = getRootURL() + "?i="+ filename;
# 			var anchor = $("<a/>");
# 			anchor.attr("target", "_blank");
# 			anchor.attr("href", shareLink);
# 			anchor.html(shareLink);
# 			shareLinkElem = $("#share_link");
# 			shareLinkElem.empty();
# 			shareLinkElem.append(anchor);
# 			if(shareFunc != null) {
# 				shareFunc();
# 				shareFunc = null;
# 			}
# 		});
# 	});
	
# 	//check query param and show img
# 	var split = document.URL.split("?i=");
# 	if(split.length > 1) {
# 		var filename = split[1];
# 		var url = getRootURL() + "i/" + filename;
# 		var $img = $("<img/>");
# 		$img.attr("src", url);
# 		var $overlay = $("<div/>").addClass("link_img_overlay");
# 		var $container = $("<div/>").addClass("container");
# 		$container.append($img);
# 		$overlay.append($container);
# 		$("#wrapper").append($overlay);
# 		$overlay.click(function(ev) {
# 			$(ev.currentTarget).fadeOut();
# 		})
# 	}
	
# 	$("#facebook_share").click(function() {
# 		if(shareLink == null) {
# 			shareFunc = facebookShare;
# 			$("#generate_link").click();
# 		}
# 		else {
# 			facebookShare();
# 		}
# 	});
	
# 	$("#twitter_share").click(function() {
# 		if(shareLink == null) {
# 			shareFunc = twitterShare;
# 			$("#generate_link").click();
# 		}
# 		else {
# 			twitterShare();
# 		}
# 	});
# });

# function getRootURL() {
# 	return document.URL.split("?")[0];
# }

# function facebookShare() {
# 	window.open("https://www.facebook.com/sharer.php?t=Super Pixel Time&u=" + shareLink);
# }

# function twitterShare() {
# 	window.open("https://twitter.com/intent/tweet?url=" + shareLink + "&via=superpixeltime&text=pixelate your life&hashtags=superpixeltime");
# }

# /**
#  * adds given palette model to the view
#  */
# function addPalette(palette, select) {
# 	var paletteElem = $("<div/>").addClass("custom_palette").attr("id", palette.name);
# 	paletteElem.click(function() {
# 		if(selectedPalette != null) {
# 			$("#" + selectedPalette.name).removeClass("selected");
# 		}
# 		selectedPalette = palette;
# 		$("#" + selectedPalette.name).addClass("selected");
# 	});
# 	$("#custom_palette_container").append(paletteElem);
	
# 	if(select) {
# 		paletteElem.click();
# 	}
	
# 	paletteHeader = $("<div/>").addClass("custom_palette_header");
# 	paletteName = $("<span/>").addClass("custom_palette_name").html(palette.name);
# 	paletteName.click(function() {
# 		var newName = prompt("Rename this palette?", palette.name);
# 		if(newName != null && palette.name != newName) {
# 			$(this).html(newName);
# 			$("#" + palette.name).attr("id", newName);
# 			palette.changeName(newName);
# 		}
# 	});
	
# 	paletteDelete = $("<span/>").addClass("custom_palette_delete").html("delete");
# 	paletteDelete.click(function() {
# 		if(confirm("Are you sure you want to delete " + palette.name)) {
# 			CustomPalette.delete(palette.name);
# 			paletteElem.remove();
# 			selectedPalette = null;
# 		}
# 	});
# 	paletteHeader.append(paletteName, paletteDelete);
	
# 	paletteColors = $("<div/>").addClass("custom_palette_colors");
# 	paletteElem.append(paletteHeader, paletteColors);
# 	var i;
# 	for(i = 0; i < palette.colors.length; i++) {
# 		var color = palette.colors[i];
# 		var colorElem = createColorElem(palette, color);
# 		paletteColors.append(colorElem);
# 	}
# }

# function createColorElem(palette, color) {
# 	var colorElem = $("<span/>").addClass("color").css('background-color', color.toBackgroundColorString());
# 	colorElem.click(function() {
# 		if(confirm("remove this color?")) {
# 			$(this).remove();
# 			palette.removeColor(color);
# 		}
# 	});
# 	return colorElem;
# }

# function fitToScreen() {
# 	if($("#fit_to_screen").attr("checked") != null) {
# 		$("canvas").css({'width':'100%'});
# 		$("#zoom_range_container").hide();
# 	}
# 	else {
# 		setCanvasZoom();
# 		$("#zoom_range_container").show();
# 	}
# }

# function setCanvasZoom() {
# 	var zoomValue = $("#zoom_range").val();
# 	$("#zoom_value").html(zoomValue + "%");
# 	var zoomValueNum = parseInt(zoomValue);
# 	zoomValueNum /= 100.0;
# 	var width = originalImage.width * zoomValueNum;
# 	$("canvas").css({'width':  width + 'px'});
# }

# function adjustWidth() {
# 	var height = parseInt($("#save_height").val());
# 	var width = originalImage.width/originalImage.height * height;
# 	width = Math.round(width);
# 	$("#save_width").val(width);
# }

# function adjustHeight() {
# 	var width = parseInt($("#save_width").val());
# 	var height = originalImage.height/originalImage.width * width;
# 	height = Math.round(height);
# 	$("#save_height").val(height);
# }

# function updateFilename() {
# 	var fileExt = "bmp";
# 	if($("#png")[0].checked) {
# 		fileExt = "png";
# 	}
# 	else if($("#jpg")[0].checked) {
# 		fileExt = "jpg";
# 	}
# 	var filename = $("#filename").val();
# 	var idx = filename.lastIndexOf(".");
# 	if(idx == -1) {
# 		idx = filename.length;
# 	}
# 	filename = filename.substr(0, idx);
# 	filename += "." + fileExt;
# 	$("#filename").val(filename);
# }

# function urlLoadHandler() {
# 	toggleLoading(true);
# 	var url = $("#url_input").val();
# 	$.getImageData({
# 		url: url,
# 		success: function(image){
# 			var split = url.split("/");
# 			var lastBit = split.length-1;
# 			if(lastBit > 0) {
# 				var filename = split[lastBit];
# 				$("#filename").val(filename);
# 			}
# 			setImage(image);
# 			toggleLoading(false);
# 		},
# 		error: function(xhr, text_status) {
# 			toggleLoading(false);
# 			alert("Invalid URL. Please enter a valid URL");
# 		}
# 	});
# }

# var img;
# function fileLoadHandler(e) {
# 	useFile = true;
# 	useURL = false;
# 	img = new Image();
# 	img.onload = function() {
# 		useFile = true;
# 	}
# 	img.src = e.target.result;
# }

# function setImage(img) {
# 	$("#instructions").hide();
# 	originalImage = img;
# 	$("#original_width").html(img.width);
# 	$("#original_height").html(img.height);
# 	//reset if needed
# 	if(canvas != null) {
# 		canvas.remove();
# 	}
# 	canvas = $("<canvas/>");
# 	var canvasElem = canvas[0];
# 	canvasElem.width = img.width;
# 	canvasElem.height = img.height;
# 	$('#save_width').val(img.width);
# 	$('#save_height').val(img.height);
	
# 	var ctx = canvasElem.getContext("2d");
# 	ctx.drawImage(img, 0, 0);
# 	$('#mainpane').append(canvas);
	
# 	$("#view_options").show();
# 	fitToScreen();
# }

# function processCanvas(canvasElem, blockSize) {
# 	var ctx = canvasElem.getContext("2d");
# 	var widthBlocks = Math.ceil(canvasElem.width / blockSize);
# 	var heightBlocks = Math.ceil(canvasElem.height / blockSize);
# 	totalNumBlocks = widthBlocks * heightBlocks;
# 	processedNumBlocks = 0;
# 	for(var x = 0; x < canvasElem.width; x += blockSize) {
# 		for(var y = 0; y < canvasElem.height; y += blockSize) {
# 			setTimeout(processBlock(ctx, x, y, canvasElem.width, canvasElem.height), 0);
# 		}
# 	}
# }

# function displayProgress() {
# 	$("#progress_blocks").html(processedNumBlocks + "/" + totalNumBlocks);
# 	$("#progress_percentage").html(Math.round(processedNumBlocks/totalNumBlocks * 100) + "%");
# }

# function processBlock(ctx, x, y, canvasWidth, canvasHeight) {
# 	return function() {
# 		if(!renderInProgress) {
# 			return;
# 		}
		
# 		var width = blockSize;
# 		if(x + blockSize >= canvasWidth) {
# 			width = canvasWidth - x;
# 		}
		
# 		var height = blockSize;
# 		if(y + blockSize >= canvasHeight) {
# 			height = canvasHeight - y;
# 		}
		
# 		var imageData = ctx.getImageData(x, y, width, height);
# 		var avgColor = avgPixel(imageData);
# 		if(selectedPalette != null) {
# 			avgColor = getClosestColor(avgColor, selectedPalette);
# 		}
# 		setImageData(imageData, avgColor);
# 		ctx.putImageData(imageData, x, y);
		
# 		processedNumBlocks++;
# 		displayProgress();
		
# 		if(processedNumBlocks == totalNumBlocks) {
# 			$("#generateButton").html("RENDER");
# 			renderInProgress = false;
			
# 			//embed logo
# 			if($("#remove_logo").attr("checked") == null) {
# 				var size = Math.min(canvasWidth * .15, canvasHeight * .15);
# 				//size should be between 50 and 150 px
# 				size = Math.min(size, 150);
# 				size = Math.max(size, 50);
# 				var embedX = canvasWidth - size - 10;
# 				var embedY = canvasHeight - size - 10;
# 				ctx.drawImage(embedLogo, embedX, embedY, size, size);
# 			}			
# 		}
# 	};
# }



# //TODO optimize
# function getClosestColor(c, palette) {
# 	var minDelta = 255*3;
# 	var closestColor;
# 	var i;
# 	for(i = 0; i < palette.colors.length; i++) {
# 		var color = palette.colors[i];
# 		var delta = c.diff(color.r, color.g, color.b);
# 		if(delta < minDelta) {
# 			minDelta = delta;
# 			closestColor = color;
# 		}
# 	}
# 	return closestColor;
# }

# function avgPixel(imageData) {
# 	var c = new Color(0, 0, 0, 0);
# 	for(var i = 0; i < imageData.data.length; i+=4) {
# 		c.r += imageData.data[i];
# 		c.g += imageData.data[i+1];
# 		c.b += imageData.data[i+2];
# 		c.a += imageData.data[i+3];
# 	}
# 	var numPixels = imageData.data.length / 4;
# 	c.r = Math.round(c.r / numPixels);
# 	c.g = Math.round(c.g / numPixels);
# 	c.b = Math.round(c.b / numPixels);
# 	c.a = Math.round(c.a / numPixels);
# 	return c;
# }

# function setImageData(imageData, c) {
# 	for(var i = 0; i < imageData.data.length; i+=4) {
# 		imageData.data[i] = c.r;
# 		imageData.data[i+1] = c.g;
# 		imageData.data[i+2] = c.b;
# 		imageData.data[i+3] = c.a;
# 	}
# }

# var loadingInterval = null;

# function toggleLoading(toggle) {
# 	if(toggle) {
# 		$("#loading_overlay").fadeIn();
# 		loadingInterval = setInterval(function() {
# 			var dots = $("#loading_dots").html();
# 			if(dots == null) {
# 				dots = "";
# 			}
# 			if(dots.length < 3) {
# 				dots += ".";
# 			}
# 			else {
# 				dots = "";
# 			}
# 			$("#loading_dots").html(dots);
# 		}, 1000);
# 	}
# 	else {
# 		$("#loading_overlay").fadeOut();
# 		clearInterval(loadingInterval);
# 	}
# }

# function loadPresetPalette(paletteData) {
# 	var i;
# 	var colors = [];
# 	for(i = 0; i < paletteData.colors.length; i++) {
# 		var colorData = paletteData.colors[i];
# 		colors.push(new Color(colorData[0], colorData[1], colorData[2]));
# 	}
# 	paletteData.colors = colors;
# 	return paletteData;
# }
