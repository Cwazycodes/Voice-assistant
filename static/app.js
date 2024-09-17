let recognition;
let listeningForWakeWord = true;
let interimTranscript = "";

function setupRecognition() {
  if (!("webkitSpeechRecognition" in window)) {
    alert("Speech recognition not supported in this browser.");
    return;
  }

  if (recognition) {
    recognition.abort();
  }

  recognition = new webkitSpeechRecognition();
  recognition.lang = "en-US";
  recognition.interimResults = true;
  recognition.continuous = false;

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

    if (finalTranscript && listeningForWakeWord) {
      if (finalTranscript.includes("piper")) {
        listeningForWakeWord = false;
        document.getElementById("status").innerText =
          "Wake word detected. Now listening for command...";
        recognition.stop();
        setupRecognition();
      }
    } else if (finalTranscript && !listeningForWakeWord) {
      document.getElementById(
        "status"
      ).innerText = `Processing command: ${finalTranscript}`;
      recognition.stop();

      if (finalTranscript.includes("exit")) {
        document.getElementById("response").innerText = "Exiting...";
        listeningForWakeWord = true;
        return;
      } else if (finalTranscript.includes("weather")) {
        fetchWeather(finalTranscript);
      } else if (finalTranscript.includes("time")) {
        fetchTime();
      } else {
        askOpenAI(finalTranscript);
      }

      listeningForWakeWord = true;
      setupRecognition();
    }
  };

  recognition.onerror = function (event) {
    document.getElementById(
      "status"
    ).innerText = `Error occurred: ${event.error}`;
  };

  recognition.onend = function () {
    if (listeningForWakeWord) {
      setupRecognition();
    }
  };

  recognition.start();
}

function speakText(text) {
  const synth = window.speechSynthesis;
  if (!synth) {
    console.error("Text-to-Speech not supported in this browser.");
    return;
  }
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = "en-UK";
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
