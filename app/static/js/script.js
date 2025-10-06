// ------------------------------------------------
// -------------- LANGUAGE SELECTION --------------
// ------------------------------------------------

// check if 'lat' is the only language displayed

function isOnlyLanguageClassDisplayed(lang) {
	var allTags = document.getElementsByTagName('tr');  
	for (const tag of allTags) {
		if (typeof tag.className !== 'undefined') {
			if (
			  tag.className.slice(0, 3) === 'lg-' &&
			  !(tag.className.includes(lang)) &&
			  tag.style.display !== "none"
			) {
				return false;
			}
		}
	}
	return true;
}

// make 'lat' tags visible/invisible

function changeVisibility(lang) {
	allTags = document.getElementsByClassName('lg-' + lang)
	for (const tag of allTags) {
		if (tag.style.display === "none") {
			tag.style.display = "block";
		} else {
			tag.style.display = "none";
		}
	}
}

// hide/show all 'lat' tags if there is at least another language displayed

function hideShow(lang) {	
	if (!isOnlyLanguageClassDisplayed(lang)) {
		changeVisibility(lang);
	}
}