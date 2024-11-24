document.addEventListener("DOMContentLoaded", () => {
    // extract page UIElements
    const UIElements = {
        screens: {
            start: document.getElementById("screen-start"),
            mode: document.getElementById("screen-mode"),
            selection: document.getElementById("screen-selection"),
            selection2: document.getElementById("screen-selection2"),
            question: document.getElementById("screen-question"),
            information: document.getElementById("screen-information"),
            answer: document.getElementById("screen-answer"),
            guess: document.getElementById("screen-guess"),
            result: document.getElementById("screen-result"),
        },
        buttons: {
            start: document.getElementById("button-start"),
            modePepper: document.getElementById("button-pepper"),
            modeUser: document.getElementById("button-user"),
            butterfly: document.getElementById("button-butterfly"),
            butterfly2: document.getElementById("button-butterfly2"),
            chimpanzee: document.getElementById("button-chimpanzee"),
            chimpanzee2: document.getElementById("button-chimpanzee2"),
            eagle: document.getElementById("button-eagle"),
            eagle2: document.getElementById("button-eagle2"),
            frog: document.getElementById("button-frog"),
            frog2: document.getElementById("button-frog2"),
            salmon: document.getElementById("button-salmon"),
            salmon2: document.getElementById("button-salmon2"),
            snake: document.getElementById("button-snake"),
            snake2: document.getElementById("button-snake2"),
            continue: document.getElementById("button-continue"),
            question1: document.getElementById("button-question-1"),
            question2: document.getElementById("button-question-2"),
            question3: document.getElementById("button-question-3"),
            question4: document.getElementById("button-question-4"),
            question5: document.getElementById("button-question-5"),
            guess: document.getElementById("button-guess"),
            yes: document.getElementById("button-yes"),
            no: document.getElementById("button-no"),
            correct: document.getElementById("button-correct"),
            incorrect: document.getElementById("button-incorrect"),
            replay: document.getElementById("button-replay"),
        },
        messages: {
            question: document.getElementById("message-question"),
            answer: document.getElementById("message-answer"),
            guess: document.getElementById("message-guess"),
            result: document.getElementById("message-result"),
        },
        images: {
            butterfly2: document.getElementById("image-butterfly2"),
            chimpanzee2: document.getElementById("image-chimpanzee2"),
            eagle2: document.getElementById("image-eagle2"),
            frog2: document.getElementById("image-frog2"),
            salmon2: document.getElementById("image-salmon2"),
            snake2: document.getElementById("image-snake2"),
            guess: document.getElementById("image-guess"),
            result: document.getElementById("image-result"),
        }
    };

    const animals = {
        butterfly: {
            name: "butterfly",
            path: "butterfly-7x5.jpg",
            legs: false,
            mammal: false,
            fly: true,
            insect: true,
            swim: false,
        },
        chimpanzee: {
            name: "chimpanzee",
            path: "chimpanzee-7x5.jpg",
            legs: true,
            mammal: true,
            fly: false,
            insect: false,
            swim: false,
        },
        eagle: {
            name: "eagle",
            path: "eagle-7x5.jpg",
            legs: false,
            mammal: false,
            fly: true,
            insect: false,
            swim: false,
        },
        frog: {
            name: "frog",
            path: "frog-7x5.jpg",
            legs: true,
            mammal: false,
            fly: false,
            insect: false,
            swim: false,
        },
        salmon: {
            name: "salmon",
            path: "salmon-7x5.jpg",
            legs: false,
            mammal: false,
            fly: false,
            insect: false,
            swim: true,
        },
        snake: {
            name: "snake",
            path: "snake-7x5.jpg",
            legs: false,
            mammal: false,
            fly: false,
            insect: false,
            swim: false,
        },
    }

    const defaultQuestions = {
        question1: "does it have legs?",
        question2: "is it a mammal?",
        question3: "does it fly?",
        question4: "is it an insect?",
        question5: "does it swim?",
    }

    // questions decision tree
    const questions = [
        { yes: 1, no: 2, text: defaultQuestions.question1, path: null },                              // 00
        { yes: 6, no: 8, text: defaultQuestions.question2, path: null },                                 // 01
        { yes: 3, no: 4, text: defaultQuestions.question3, path: null },                                    // 02
        { yes: 5, no: 7, text: defaultQuestions.question4, path: null },                                // 03
        { yes: 9, no: 10, text: defaultQuestions.question5, path: null },                                  // 04
        { yes: null, no: null, text: animals.butterfly.name, path: animals.butterfly.path },    // 05
        { yes: null, no: null, text: animals.chimpanzee.name, path: animals.chimpanzee.path },  // 06
        { yes: null, no: null, text: animals.eagle.name, path: animals.eagle.path },            // 07
        { yes: null, no: null, text: animals.frog.name, path: animals.frog.path },              // 08
        { yes: null, no: null, text: animals.salmon.name, path: animals.salmon.path },          // 09
        { yes: null, no: null, text: animals.snake.name, path: animals.snake.path },            // 10
    ];

    let currentQuestion = 0;
    let selectedAnimal = 'chimpanzee';
    let isGuess = true;
    let isGuessCorrect = true;

    // Utility functions
    const switchScreen = (hide, show) => {
        hide.classList.add("hidden");
        show.classList.remove("hidden");
    };

    const pickRandomAnimal = () => {
        // Get all keys from the animals object
        const animalKeys = Object.keys(animals);

        // Choose a random key
        const randomKey = animalKeys[Math.floor(Math.random() * animalKeys.length)];

        // Return the selected animal object
        return animals[randomKey].name;
    };

    const updateMessage = (element, text) => {
        UIElements.messages[element].textContent = text;
    };

    const updateImage = (image, path, isRedScale = false) => {
        const imageElement = UIElements.images[image];

        if (imageElement) {
            imageElement.src = `/interface/assets/images/${path}`;
            imageElement.style.filter = isRedScale
                ? "grayscale(100%) sepia(100%) saturate(500%) hue-rotate(-50deg)"
                : "none";
        } else {
            console.error(`Element with id "${image}" not found.`);
        }
    };

    const sendData = () => {
        fetch('http://127.0.0.1:5000/guess-game', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                animal: questions[currentQuestion].text,
                selectedAnimal: selectedAnimal,
                isGuess: isGuess,
                isGuesser: isGuessCorrect,
            }),
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error))
    };

    // Handle answers (Yes/No) in the decision tree
    const handleQuestion = (answer) => {
        currentQuestion = questions[currentQuestion][answer];
        updateMessage("question", questions[currentQuestion].text);

        if (questions[currentQuestion].yes === questions[currentQuestion].no) {
            updateMessage("guess", `is it a ${questions[currentQuestion].text}?`);
            updateImage("guess", questions[currentQuestion].path);
            switchScreen(UIElements.screens.question, UIElements.screens.guess);
        }
    };

    UIElements.buttons.yes.addEventListener("click", () => handleQuestion("yes"));
    UIElements.buttons.no.addEventListener("click", () => handleQuestion("no"));

    UIElements.buttons.correct.addEventListener("click", () => {
        switchScreen(UIElements.screens.guess, UIElements.screens.result);

        updateMessage("result", `it's a ${questions[currentQuestion].text}!`);
        updateImage("result", questions[currentQuestion].path, false);
    });

    UIElements.buttons.incorrect.addEventListener("click", () => {
        isGuessCorrect = false;
        switchScreen(UIElements.screens.guess, UIElements.screens.result);

        updateMessage("result", `it's not a ${questions[currentQuestion].text}?`);
        updateImage("result", questions[currentQuestion].path, true);
    });

    // Event listeners
    const buttonActions = {
        start: () => {
            switchScreen(UIElements.screens.start, UIElements.screens.mode);
        },
        modePepper: () => {
            switchScreen(UIElements.screens.mode, UIElements.screens.selection);
        },
        modeUser: () => {
            isGuess = false;

            switchScreen(UIElements.screens.mode, UIElements.screens.information);
        },
        butterfly: () => {
            currentQuestion = 0;
            selectedAnimal = 'butterfly';

            updateMessage("question", questions[currentQuestion].text);
            switchScreen(UIElements.screens.selection, UIElements.screens.question);
        },
        chimpanzee: () => {
            currentQuestion = 0;
            selectedAnimal = 'chimpanzee';

            updateMessage("question", questions[currentQuestion].text);
            switchScreen(UIElements.screens.selection, UIElements.screens.question);
        },
        eagle: () => {
            currentQuestion = 0;
            selectedAnimal = 'eagle';

            updateMessage("question", questions[currentQuestion].text);
            switchScreen(UIElements.screens.selection, UIElements.screens.question);
        },
        frog: () => {
            currentQuestion = 0;
            selectedAnimal = 'frog';

            updateMessage("question", questions[currentQuestion].text);
            switchScreen(UIElements.screens.selection, UIElements.screens.question);
        },
        salmon: () => {
            currentQuestion = 0;
            selectedAnimal = 'salmon';

            updateMessage("question", questions[currentQuestion].text);
            switchScreen(UIElements.screens.selection, UIElements.screens.question);
        },
        snake: () => {
            currentQuestion = 0;
            selectedAnimal = 'snake';

            updateMessage("question", questions[currentQuestion].text);
            switchScreen(UIElements.screens.selection, UIElements.screens.question);
        },
        butterfly2: () => {
            if (animals[selectedAnimal].name === "butterfly") {
                switchScreen(UIElements.screens.selection2, UIElements.screens.result);
                updateMessage("result", "it's a butterfly!")
                updateImage("result", animals["butterfly"].path)
            } else {
                UIElements.buttons.butterfly2.disabled = true;
                UIElements.images.butterfly2.style.filter = "grayscale(100%)"
            }
        },
        chimpanzee2: () => {
            if (animals[selectedAnimal].name === "chimpanzee") {
                switchScreen(UIElements.screens.selection2, UIElements.screens.result);
                updateMessage("result", "it's a chimpanzee!")
                updateImage("result", animals["chimpanzee"].path)
            } else {
                UIElements.buttons.chimpanzee2.disabled = true;
                UIElements.images.chimpanzee2.style.filter = "grayscale(100%)"
            }
        },
        eagle2: () => {
            if (animals[selectedAnimal].name === "eagle") {
                switchScreen(UIElements.screens.selection2, UIElements.screens.result);
                updateMessage("result", "it's a eagle!")
                updateImage("result", animals["eagle"].path)
            } else {
                UIElements.buttons.eagle2.disabled = true;
                UIElements.images.eagle2.style.filter = "grayscale(100%)"
            }
        },
        frog2: () => {
            if (animals[selectedAnimal].name === "frog") {
                switchScreen(UIElements.screens.selection2, UIElements.screens.result);
                updateMessage("result", "it's a frog!")
                updateImage("result", animals["frog"].path)
            } else {
                UIElements.buttons.frog2.disabled = true;
                UIElements.images.frog2.style.filter = "grayscale(100%)"
            }
        },
        salmon2: () => {
            if (animals[selectedAnimal].name === "salmon") {
                switchScreen(UIElements.screens.selection2, UIElements.screens.result);
                updateMessage("result", "it's a salmon!")
                updateImage("result", animals["salmon"].path)
            } else {
                UIElements.buttons.salmon2.disabled = true;
                UIElements.images.salmon2.style.filter = "grayscale(100%)"
            }
        },
        snake2: () => {
            if (animals[selectedAnimal].name === "snake") {
                switchScreen(UIElements.screens.selection2, UIElements.screens.result);
                updateMessage("result", "it's a snake!")
                updateImage("result", animals["snake"].path)
            } else {
                UIElements.buttons.snake2.disabled = true;
                UIElements.images.snake2.style.filter = "grayscale(100%)"
            }
        },
        question1: () => {
            if (animals[selectedAnimal]["legs"]) {
                UIElements.buttons.question1.style.backgroundColor = "rgba(0, 128, 0, 0.250)";
                UIElements.buttons.question1.textContent = UIElements.buttons.question1.textContent + " yes!";
            } else {
                UIElements.buttons.question1.style.backgroundColor = "rgba(128, 0, 0, 0.250)";
                UIElements.buttons.question1.textContent = UIElements.buttons.question1.textContent + " no!";
            }

            UIElements.buttons.question1.disabled = true;

            if (UIElements.buttons.question1.disabled && UIElements.buttons.question2.disabled && UIElements.buttons.question3.disabled && UIElements.buttons.question4.disabled && UIElements.buttons.question5.disabled) {
                UIElements.buttons.guess.disabled = false;
            }
        },
        question2: () => {
            if (animals[selectedAnimal]["mammal"]) {
                UIElements.buttons.question2.style.backgroundColor = "rgba(0, 128, 0, 0.250)";
                UIElements.buttons.question2.textContent = UIElements.buttons.question2.textContent + " yes!";
            } else {
                UIElements.buttons.question2.style.backgroundColor = "rgba(128, 0, 0, 0.250)";
                UIElements.buttons.question2.textContent = UIElements.buttons.question2.textContent + " no!";
            }

            UIElements.buttons.question2.disabled = true;

            if (UIElements.buttons.question1.disabled && UIElements.buttons.question2.disabled && UIElements.buttons.question3.disabled && UIElements.buttons.question4.disabled && UIElements.buttons.question5.disabled) {
                UIElements.buttons.guess.disabled = false;
            }
        },
        question3: () => {
            if (animals[selectedAnimal]["fly"]) {
                UIElements.buttons.question3.style.backgroundColor = "rgba(0, 128, 0, 0.250)";
                UIElements.buttons.question3.textContent = UIElements.buttons.question3.textContent + " yes!";
            } else {
                UIElements.buttons.question3.style.backgroundColor = "rgba(128, 0, 0, 0.250)";
                UIElements.buttons.question3.textContent = UIElements.buttons.question3.textContent + " no!";
            }

            UIElements.buttons.question3.disabled = true;

            if (UIElements.buttons.question1.disabled && UIElements.buttons.question2.disabled && UIElements.buttons.question3.disabled && UIElements.buttons.question4.disabled && UIElements.buttons.question5.disabled) {
                UIElements.buttons.guess.disabled = false;
            }
        },
        question4: () => {
            if (animals[selectedAnimal]["insect"]) {
                UIElements.buttons.question4.style.backgroundColor = "rgba(0, 128, 0, 0.250)";
                UIElements.buttons.question4.textContent = UIElements.buttons.question4.textContent + " yes!";
            } else {
                UIElements.buttons.question4.style.backgroundColor = "rgba(128, 0, 0, 0.250)";
                UIElements.buttons.question4.textContent = UIElements.buttons.question4.textContent + " no!";
            }

            UIElements.buttons.question4.disabled = true;

            if (UIElements.buttons.question1.disabled && UIElements.buttons.question2.disabled && UIElements.buttons.question3.disabled && UIElements.buttons.question4.disabled && UIElements.buttons.question5.disabled) {
                UIElements.buttons.guess.disabled = false;
            }
        },
        question5: () => {
            if (animals[selectedAnimal]["swim"]) {
                UIElements.buttons.question5.style.backgroundColor = "rgba(0, 128, 0, 0.250)";
                UIElements.buttons.question5.textContent = UIElements.buttons.question5.textContent + " yes!";
            } else {
                UIElements.buttons.question5.style.backgroundColor = "rgba(128, 0, 0, 0.250)";
                UIElements.buttons.question5.textContent = UIElements.buttons.question5.textContent + " no!";
            }

            UIElements.buttons.question5.disabled = true;

            if (UIElements.buttons.question1.disabled && UIElements.buttons.question2.disabled && UIElements.buttons.question3.disabled && UIElements.buttons.question4.disabled && UIElements.buttons.question5.disabled) {
                UIElements.buttons.guess.disabled = false;
            }
        },
        continue: () => {
            UIElements.buttons.question1.textContent = defaultQuestions.question1
            UIElements.buttons.question2.textContent = defaultQuestions.question2
            UIElements.buttons.question3.textContent = defaultQuestions.question3
            UIElements.buttons.question4.textContent = defaultQuestions.question4
            UIElements.buttons.question5.textContent = defaultQuestions.question5

            UIElements.buttons.question1.style.backgroundColor = "#007bff"
            UIElements.buttons.question2.style.backgroundColor = "#007bff"
            UIElements.buttons.question3.style.backgroundColor = "#007bff"
            UIElements.buttons.question4.style.backgroundColor = "#007bff"
            UIElements.buttons.question5.style.backgroundColor = "#007bff"

            UIElements.buttons.question1.disabled = false;
            UIElements.buttons.question2.disabled = false;
            UIElements.buttons.question3.disabled = false;
            UIElements.buttons.question4.disabled = false;
            UIElements.buttons.question5.disabled = false;
            UIElements.buttons.guess.disabled = true;

            selectedAnimal = pickRandomAnimal()

            switchScreen(UIElements.screens.information, UIElements.screens.answer);
        },
        guess: () => {
            UIElements.buttons.butterfly2.disabled = false;
            UIElements.buttons.chimpanzee2.disabled = false;
            UIElements.buttons.eagle2.disabled = false;
            UIElements.buttons.frog2.disabled = false;
            UIElements.buttons.salmon2.disabled = false;
            UIElements.buttons.snake2.disabled = false;

            UIElements.images.butterfly2.style.filter = "none"
            UIElements.images.chimpanzee2.style.filter = "none"
            UIElements.images.eagle2.style.filter = "none"
            UIElements.images.frog2.style.filter = "none"
            UIElements.images.salmon2.style.filter = "none"
            UIElements.images.snake2.style.filter = "none"

            switchScreen(UIElements.screens.answer, UIElements.screens.selection2);


        },
        replay: () => {
            switchScreen(UIElements.screens.result, UIElements.screens.start)
            sendData()

            currentQuestion = 0;
            selectedAnimal = 'chimpanzee';
            isGuess = true;
            isGuessCorrect = true;
        }
    };

    Object.entries(buttonActions).forEach(([buttonName, action]) => {
        UIElements.buttons[buttonName].addEventListener("click", action);
    });
});
