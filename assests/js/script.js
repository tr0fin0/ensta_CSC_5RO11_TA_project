document.addEventListener("DOMContentLoaded", () => {
    const startScreen = document.getElementById("screen-start");
    const questionScreen = document.getElementById("screen-question");
    const endScreen = document.getElementById("screen-result");

    const startButton = document.getElementById("button-start-guess");
    const yesButton = document.getElementById("button-yes");
    const noButton = document.getElementById("button-no");
    const restartButton = document.getElementById("button-restart");

    const questionElement = document.getElementById("message-question");
    const resultMessage = document.getElementById("message-result");

    // Questions data structure
    const questions = [
        { yes: 1, no: 2, text: "Does it have legs?" },      // 00
        { yes: 6, no: 8, text: "Is it a mammal?" },         // 01
        { yes: 3, no: 4, text: "Does it fly?" },            // 02
        { yes: 5, no: 7, text: "Is it an insect?" },        // 03
        { yes: 9, no: 10, text: "Does it swim?" },          // 04
        { yes: null, no: null, text: "It's a Butterfly!" }, // 05
        { yes: null, no: null, text: "It's a Chimpanzee!" },// 06
        { yes: null, no: null, text: "It's a Eagle!" },     // 07
        { yes: null, no: null, text: "It's a Frog!" },      // 08
        { yes: null, no: null, text: "It's a Salmon!" },    // 09
        { yes: null, no: null, text: "It's a Snake!" },     // 10
    ];

    let currentQuestionIndex = 0;

    // Helper to switch screens
    const switchScreen = (hide, show) => {
        hide.classList.add("hidden");
        show.classList.remove("hidden");
    };

    // Event listeners
    startButton.addEventListener("click", () => {
        currentQuestionIndex = 0;
        questionElement.textContent = questions[currentQuestionIndex].text;

        switchScreen(startScreen, questionScreen);
    });

    yesButton.addEventListener("click", () => handleAnswer("yes"));
    noButton.addEventListener("click", () => handleAnswer("no"));

    restartButton.addEventListener("click", () => {
        switchScreen(endScreen, startScreen);
    });

    const handleAnswer = (answer) => {
        const nextIndex = questions[currentQuestionIndex][answer];

        if (nextIndex === null) {
            switchScreen(questionScreen, endScreen);

            resultMessage.textContent = questions[currentQuestionIndex].text;
        } else {
            currentQuestionIndex = nextIndex;
            questionElement.textContent = questions[currentQuestionIndex].text;
        }
    };
});
