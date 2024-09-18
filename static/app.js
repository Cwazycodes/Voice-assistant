let recognition;
let listeningForWakeWord = true;
let interimTranscript = "";
let isSpeaking = false;

function setupRecognition() {
  if (!("webkitSpeechRecognition" in window)) {
    alert("Speech recognition not supported in this browser.");
    return;
  }

  if (recognition) {
    recognition.stop();
  }

  recognition = new webkitSpeechRecognition();
  recognition.lang = "en-US";
  recognition.interimResults = true;
  recognition.continuous = true;

  recognition.onstart = function () {
    document.getElementById("status").innerText = listeningForWakeWord
      ? "Listening for the wake word..."
      : "Listening for your command...";
  };

  recognition.onresult = function (event) {
    interimTranscript = "";
    let finalTranscript = "";

    for (let i = event.resultIndex; i < event.results.length; ++i) {
      if (event.results[i].isFinal) {
        finalTranscript += event.results[i][0].transcript.toLowerCase().trim();
      } else {
        interimTranscript += event.results[i][0].transcript
          .toLowerCase()
          .trim();
      }
    }

    document.getElementById("transcription").innerText =
      interimTranscript || finalTranscript;

    if (finalTranscript) {
      if (listeningForWakeWord) {
        if (finalTranscript.includes("piper")) {
          listeningForWakeWord = false;
          handleWakeWordDetection();
        }
      } else {
        handleUserCommand(finalTranscript);
      }
    }
  };

  recognition.onerror = function (event) {
    document.getElementById("status").innerText = `Error: ${event.error}`;
    if (event.error === "not-allowed") {
      document.getElementById("status").innerText =
        "Microphone blocked. Please allow access.";
    }
  };

  recognition.onend = function () {
    if (!isSpeaking) {
      setupRecognition();
    }
  };

  recognition.start();
}

function handleWakeWordDetection() {
  const responses = ["How can I help you?", "Yes?"];
  const response = responses[Math.floor(Math.random() * responses.length)];

  document.getElementById("status").innerText =
    "Wake word detected. Now listening for command...";
  speakText(response);
}

function handleUserCommand(command) {
  document.getElementById(
    "status"
  ).innerText = `Processing command: ${command}`;

  if (command.includes("exit")) {
    document.getElementById("response").innerText = "Exiting...";
    speakText("Exiting...");
    listeningForWakeWord = true;
  } else if (command.includes("weather")) {
    fetchWeather(command);
  } else if (command.includes("time")) {
    fetchTime();
  } else {
    askOpenAI(command);
  }
}

function speakText(text) {
  const synth = window.speechSynthesis;
  if (!synth) {
    return;
  }

  isSpeaking = true;

  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = "en-UK";

  if (recognition) {
    recognition.stop();
  }

  utterance.onstart = function () {
    document.getElementById("status").innerText = "Speaking...";
  };

  utterance.onend = function () {
    isSpeaking = false;
    document.getElementById("status").innerText =
      "Finished speaking. Listening again...";

    setupRecognition();
  };

  synth.speak(utterance);
}

function fetchWeather(command) {
  const city = extractCityFromCommand(command);

  if (!city) {
    const errorMsg = "Please specify a city for the weather.";
    document.getElementById("response").innerText = errorMsg;
    speakText(errorMsg);
    return;
  }

  fetch("/weather", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ city: city }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.weather) {
        document.getElementById("response").innerText = data.weather;
        speakText(data.weather);
      } else {
        const errorMsg = "Could not retrieve weather information.";
        document.getElementById("response").innerText = errorMsg;
        speakText(errorMsg);
      }
    })
    .catch((error) => {
      console.error("Error fetching weather:", error);
      const errorMsg = "Error fetching weather information.";
      document.getElementById("response").innerText = errorMsg;
      speakText(errorMsg);
    });
}

function fetchTime() {
  fetch("/time", {
    method: "GET",
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.time) {
        document.getElementById("response").innerText = data.time;
        speakText(data.time);
      } else {
        const errorMsg = "Could not retrieve the time.";
        document.getElementById("response").innerText = errorMsg;
        speakText(errorMsg);
      }
    })
    .catch((error) => {
      console.error("Error fetching time:", error);
      const errorMsg = "Error fetching time.";
      document.getElementById("response").innerText = errorMsg;
      speakText(errorMsg);
    });
}

function askOpenAI(command) {
  fetch("/ask", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ command: command }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.response) {
        document.getElementById("response").innerText = data.response;
        speakText(data.response);
      } else {
        const errorMsg = "Could not get a response from OpenAI.";
        document.getElementById("response").innerText = errorMsg;
        speakText(errorMsg);
      }
    })
    .catch((error) => {
      console.error("Error fetching response from OpenAI:", error);
      const errorMsg = "Error processing your command.";
      document.getElementById("response").innerText = errorMsg;
      speakText(errorMsg);
    });
}

function extractCityFromCommand(command) {
  const cityMatch = command.match(/weather (in|like in|for) ([a-zA-Z\s]+)/i);
  if (cityMatch && cityMatch[2]) {
    return cityMatch[2].trim();
  }
  return null;
}

window.onload = function () {
  setupRecognition();
};
