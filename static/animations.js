const links = document.getElementsByClassName('link');
	for (let i = 0; i <= links.length; i++) {
		links[i].addEventListener('mouseover', function() {
			links[i].classList.add('grown');
			links[i].classList.remove('shrunken');
		});
			links[i].addEventListener('mouseout', function() {
			links[i].classList.remove('grown');
			links[i].classList.add('shrunken');
		});
	}
	
	function shift() {

		// Preventing the user from accidentally closing the window
		document.title = "Your ppt is being made";

		// Darkening the video background
		const video = document.getElementById('video-bg');
		video.classList.add('darkened')
		
		// Fading and deleting the unnecessary elements
		const fade1 = document.getElementById('fade1');
		const fade2 = document.getElementById('fade2');
		const fade3 = document.getElementById('fade3');
		const fade4 = document.getElementById('fade4');
		const fade5 = document.getElementById('fade5');
		const fade6 = document.getElementById('fade6');
		const fade7 = document.getElementById('fade7');
		const fade8 = document.getElementById('fade8');
		const logo = document.getElementById('logo');
		fade1.style.opacity = '0';
		fade2.style.opacity = '0';
		fade3.style.opacity = '0';
		fade4.style.opacity = '0';
		fade5.style.opacity = '0';
		fade6.style.opacity = '0';
		fade7.style.opacity = '0';
		fade8.style.opacity = '0';
		logo.style.opacity = '0';
		setTimeout(function(){fade8.parentNode.removeChild(fade8);}, 1000);
		setTimeout(function(){logo.parentNode.removeChild(logo);}, 1000);
		setTimeout(function(){fade1.parentNode.removeChild(fade1);}, 1000);
		setTimeout(function(){fade2.parentNode.removeChild(fade2);}, 1000);
		setTimeout(function(){fade3.parentNode.removeChild(fade3);}, 1000);
		setTimeout(function(){fade4.parentNode.removeChild(fade4);}, 1000);
		setTimeout(function(){fade5.parentNode.removeChild(fade5);}, 1000);
		setTimeout(function(){fade6.parentNode.removeChild(fade6);}, 1000);
		setTimeout(function(){fade7.parentNode.removeChild(fade7);}, 1000);
		
		// Shiftin the search/loading bar to bottom
		const bar = document.getElementById('search-bar');
		bar.classList.add('shifted');
		
		const input = document.getElementById('topic');
		input.style.color = 'transparent';

		// Making the iframe with the title ascend
		setTimeout(function() {
			const pptArea = document.createElement('div');
			pptArea.setAttribute('id', 'pptArea');

			const placeholder = document.createElement('div');
			placeholder.setAttribute('id', 'placeholder');

			const boxTitle = document.createElement('p');
			boxTitle.innerHTML = 'Look at what our other users created with Pipiton before';
			placeholder.appendChild(boxTitle);

			pptArea.appendChild(placeholder);

			const iFrame = document.createElement('iframe');
			iFrame.setAttribute('src', 'https://view.officeapps.live.com/op/view.aspx?src=[https://www.pipiton.com/name.pptx]');
		
			pptArea.appendChild(iFrame);

			const content = document.getElementById('main');
			content.appendChild(pptArea);

            // Add a tip to wait into the progress bar
			const tip = document.createElement('p');
			tip.setAttribute('id', 'tip');
            tip.innerHTML = 'Relax while bots are making your ppt'; 
			content.append(tip);

            // Add a functioning progress bar
            const progress = document.createElement('progress');
            progress.setAttribute('max', '100');
            progress.setAttribute('value', '{{ fill }}') // Put {{var}} from Flask
            content.appendChild(progress); 

			// Add this line when the Flask variable has been implemented:
			// if ({{prgrs}} == 100) { progress.style.borderRadius = 10vmin; }

		}, 1500);

		
	}