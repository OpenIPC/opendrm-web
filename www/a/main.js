// OpenDRM-web main JavaScript

document.addEventListener("DOMContentLoaded", function () {
	// Update clock
	function updateClock() {
		var el = document.getElementById("time-now");
		if (el) {
			el.textContent = new Date().toLocaleString();
		}
	}
	updateClock();
	setInterval(updateClock, 1000);

	// Toggle password visibility
	document.querySelectorAll("input[type=checkbox][data-for]").forEach(function (cb) {
		cb.addEventListener("change", function () {
			var target = document.getElementById(cb.dataset.for);
			if (target) {
				target.type = cb.checked ? "text" : "password";
			}
		});
	});

	// Auto-dismiss alerts after 5 seconds
	document.querySelectorAll(".alert[data-autohide]").forEach(function (el) {
		setTimeout(function () {
			el.style.transition = "opacity 0.5s";
			el.style.opacity = "0";
			setTimeout(function () { el.remove(); }, 500);
		}, 5000);
	});

	// Confirm dangerous actions
	document.querySelectorAll("[data-confirm]").forEach(function (el) {
		el.addEventListener("click", function (e) {
			if (!confirm(el.dataset.confirm)) {
				e.preventDefault();
			}
		});
	});

	// Mobile nav toggle
	var toggler = document.getElementById("nav-toggler");
	var navLinks = document.getElementById("nav-links");
	if (toggler && navLinks) {
		toggler.addEventListener("click", function () {
			navLinks.style.display = navLinks.style.display === "flex" ? "none" : "flex";
		});
	}
});
