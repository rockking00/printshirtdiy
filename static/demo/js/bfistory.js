const backBtn = document.querySelector('#back-button');
const forwardBtn = document.querySelector('#forward-button');

function goBack(event) {
    event.preventDefault();
    if (localStorage.getItem('disableLocalStorage') === 'true') {
        localStorage.removeItem('disableLocalStorage');
    } else {
        window.history.back();
    }
}

function goForward(event) {
    event.preventDefault();
    if (localStorage.getItem('disableLocalStorage') === 'true') {
        localStorage.removeItem('disableLocalStorage');
    } else {
        window.history.forward();
    }
}

backBtn.addEventListener('click', goBack);
forwardBtn.addEventListener('click', goForward)