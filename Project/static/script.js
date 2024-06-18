const elements = document.getElementsByClassName('delay');

function addClassAfterDelay() {
    for (let i = 0; i < elements.length; i++) {
        // Using a closure to capture the current value of i
        setTimeout(function (index) {
            return function () {
                removeAdd(elements[index]);
            };
        }(i), i * 20); // Delay increases with each iteration (0s, 2s, 4s, ...)
    }
}

function removeAdd(emt) {
    emt.classList.remove('hidden');
    emt.classList.add('animation');
}

addClassAfterDelay();






// for showing filter input box
function filter() {
    var myin = document.getElementById("myInput");
    console.log(myin)
    myin.classList.remove('display-none');
}



// used for filtering books and sections by their name and authors name
function myFunction() {
    var input, filter, all, that_col, title;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    all = document.getElementById("all");
    that_col = document.getElementsByClassName("that_col");
    for (var i = 0; i < that_col.length; i++) {
        title = that_col[i].getElementsByClassName(`title${i + 1}`)[0];
        author = that_col[i].getElementsByClassName(`author${i + 1}`)[0];
                
        if (author){
            console.log(title)
            console.log(author)
            titleValue = title.textContent || title.innerText;
            authorValue = author.textContent || author.innerText;
            if (titleValue.toUpperCase().indexOf(filter) > -1 || authorValue.toUpperCase().indexOf(filter) > -1){
                that_col[i].style.display = "";
            } else {
                that_col[i].style.display = "none";
            }
        } else {
            console.log(title)
            titleValue = title.textContent || title.innerText;
            if (titleValue.toUpperCase().indexOf(filter) > -1){
                that_col[i].style.display = "";
            } else {
                that_col[i].style.display = "none";
            }
        }
    }
}


// used for filtering readers by their username at all readers page
function myreadersFunction() {
    var input, filter, all, that_col, title;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    all = document.getElementById("all");
    that_col = document.getElementsByClassName("that_col");
    for (var i = 0; i < that_col.length; i++) {
        username = that_col[i].getElementsByClassName(`username${i + 1}`)[0];
        console.log(username)
        usernameValue = username.textContent || username.innerText;

        if (usernameValue.toUpperCase().indexOf(filter) > -1 ){
            that_col[i].style.display = "";
        } else {
            that_col[i].style.display = "none";
        }
    }
}



// for filtering requests by their book's names , requester's name or duration
function myrequestsFunction() {
    var input, filter, all, that_col, title;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    all = document.getElementById("all");
    that_col = document.getElementsByClassName("that_col");
    for (var i = 0; i < that_col.length; i++) {
        book = that_col[i].getElementsByClassName(`book${i + 1}`)[0];
        user = that_col[i].getElementsByClassName(`user${i + 1}`)[0];
        // section = that_col[i].getElementsByClassName(`section${i + 1}`)[0];
        duration = that_col[i].getElementsByClassName(`duration${i + 1}`)[0];

        bookValue = book.textContent || book.innerText;
        userValue = user.textContent || user.innerText;
        // sectionValue = section.textContent || section.innerText;
        durationValue = duration.textContent || duration.innerText;
        if (bookValue.toUpperCase().indexOf(filter) > -1 || userValue.toUpperCase().indexOf(filter) > -1 || // sectionValue.toUpperCase().indexOf(filter) > -1 ||
        durationValue.toUpperCase().indexOf(filter) > -1) {
            that_col[i].style.display = "";
            console.log(that_col[i].nextElementSibling);
            that_col[i].nextElementSibling.style.display = "";
        } else {
            that_col[i].style.display = "none";
            console.log(that_col[i].nextElementSibling);
            that_col[i].nextElementSibling.style.display = "none";
        }
    }
}




// for add book to section's - form 
function triggerElement(element) {
    console.log(element);
    var i = element.id[element.id.length - 1];
    console.log(i);
    var targetElement = document.getElementById('targetElement'+i);
    console.log(targetElement);
    targetElement.click();
}


function triggerElementFromShowSection() {
    var targetElement = document.getElementById('targetElementFromShowSection');
    console.log(targetElement);
    targetElement.click();
}





// speaker for pdf 
function speaker(element) {
    console.log(element.parentNode.parentNode);
    var pdfPath = element.parentNode.parentNode.nextElementSibling.getElementsByTagName('embed')[0].src;
    var hidden = element.nextElementSibling;
    hidden.classList.remove('display-none');
    console.log(pdfPath);
    var pdfUrl = pdfPath;

    fetch(pdfUrl)
    .then(response => response.arrayBuffer())
    .then(arrayBuffer => {
        pdfjsLib.getDocument(arrayBuffer).promise.then(function(pdf) {
            var numPages = pdf.numPages;
            var pdfContent = '';
            var promises = [];
            for (var i = 1; i <= numPages; i++) {
                promises.push(pdf.getPage(i).then(function(page) {
                    return page.getTextContent().then(function(textContent) {
                        var text = '';
                        textContent.items.forEach(function(item) {
                            text += item.str + ' ';
                        });
                        pdfContent += text;
                    });
                }));
            }
            
            Promise.all(promises).then(function() {
                
                console.log(pdfContent);
                let synth = window.speechSynthesis;
                let voice = new SpeechSynthesisUtterance(pdfContent);
                voice.rate = 0.8;
                synth.speak(voice);

                document.addEventListener('keydown', function(event) {
                    if (event.key === 'm') {
                        synth.cancel();
                        hidden.classList.add('display-none'); 
                    }
                });
            });
        });
    })
    .catch(error => {
        console.error('Error fetching PDF:', error);
    });
}


// speaker for description
function speakerForDescription(element) {
    console.log(element);
    console.log(element.nextElementSibling); 
    element.nextElementSibling.classList.remove('display-none'); 
    console.log(element.parentNode); 
    console.log(element.parentNode.nextElementSibling);  
    console.log(element.parentNode.nextElementSibling.nextElementSibling);  
    var content = element.parentNode.nextElementSibling.nextElementSibling.innerText;   
    console.log(content);
    let synth = window.speechSynthesis;
    let voice = new SpeechSynthesisUtterance(content);
    voice.rate = 0.7;
    synth.speak(voice);

    document.addEventListener('keydown', function(event) {
        if (event.key === 'm') {
            synth.cancel();
            element.nextElementSibling.classList.add('display-none'); 
        }
    });
}



