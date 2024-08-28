#!/usr/bin/node


document.addEventListener("DOMContentLoaded", function() {
	const form = document.querySelector("form");

	form.addEventListener("submit", function(event) {
		// Get form field values
		const conductResearch = document.getElementById("conductResearch").value.trim();
		const totalSales = document.getElementById("totalSales").value.trim();
		const campaignType = document.getElementById("campaignType").value;
		const campaignDate = document.getElementById("campaignDate").value;

		// Validate Conduct Research field
		if (conductResearch === "") {
			alert("Please enter the research name.");
			event.preventDefault();
			return;
		}

		// Validate Total Sales field - must be a number
		if (totalSales === "" || isNaN(totalSales)) {
			alert("Press enter a valid number for Total Sales.");
			event.presentDefault();
			return;
		}

		// VValidate Campaign Type field
		if (campaignType === "") {
			alert("Press select campaign type.")
			event.presentDefault();
			return;
		}
	}
}
