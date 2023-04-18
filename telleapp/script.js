// Henter elementer fra DOM
let topEl = document.querySelector('.top')
let leftEl = document.querySelector('.left')
let rightEl = document.querySelector('.right')

// Sjekker om tall eksisterer i localStorage
if(!localStorage.tall){
    localStorage.tall = 0
}

// Oppdaterer tallet i HTML
topEl.innerHTML = localStorage.tall


// Letter til lyttere
leftEl.addEventListener('click', decreaseNumber)
rightEl.addEventListener('click', increaseNumber)

// Funksjon som minker tallet
function decreaseNumber(){
    // Minker verdien med 1
    localStorage.tall = Number(localStorage.tall) - 1

    // Oppdaterer HTML
    topEl.innerHTML = localStorage.tall
}

// Funksjon som øker tallet
function increaseNumber(){
    // Øker verdien med 1
    localStorage.tall = Number(localStorage.tall) + 1

    // Oppdaterer HTML
    topEl.innerHTML = localStorage.tall
}