const dataPrompt = localStorage.getItem('promptInput');
const divClick = document.querySelectorAll('.style_text');
const textareaText = document.querySelector('#prompt')
const generateBtn = document.querySelector('#generate-btn')
divClick.forEach(function (div) {
    div.addEventListener('click', function () {
        const textSpan = div.querySelector('.spantext');
        const textContent = textSpan.textContent.trim();
        const styles = {
            'Oil Painting': 'Oil Painting',
            'Digital Art': 'Digital Art',
            'Graphic Art': 'Trending on ArtStation',
            'Watercolor': 'watercolor painting in the style of John James Audubon',
            'Retro': 'retro poster, illustration',
            'Steampunk': 'steampunk painting',
            'Cartoon': 'still from a Studio Ghibli cartoon, anime',
            'Pencil Art': 'pencil sketch',
            'One Line': 'one line drawing, black and white',
            'Abstract': 'abstract painting',
            'Vivid Colors': 'Vivid Colors Oil painting style',
            'B&W': 'black and white colors Oil painting style',
            'Earth Tones': 'earth tone colors Oil painting style',
            'Reds': 'red and orange colors Oil painting style',
            'Coral & Teal': 'coral and teal colors Oil painting style',
            'Green': 'green colors Oil painting style',
            'Yellow': 'yellow colors Oil painting style'
        }
        if (styles[textContent]) {
            window.localStorage.setItem('promptInput', dataPrompt + ', ' + styles[textContent]);
            textareaText.value = dataPrompt + ', ' + styles[textContent];
            generateBtn.classList.add('ring-4', 'ring-pink-600', 'ring-inset', 'ring-opacity-50','animate-pulse')
        }
    })
})
