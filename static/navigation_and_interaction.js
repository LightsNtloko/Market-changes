#!/usr/bin/node

// Smooth scroll for navigation links
document.querySelectorAll('nav ul li a').forEach(link => {
	link.addEventListener('click', function(e) {
		e.preventDefault();
		const target = document.querySelector(this.getAttribute('href'));
		target.scrollIntoView({
			behavior: 'smooth'
		});
	});
})
