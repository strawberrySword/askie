const html = `
  <div style="text-align: center;">
    <button id="mic-btn" style="padding: 10px 20px; font-size: 18px;">🎤 Click to Speak</button>
    <p id="result" style="font-size: 20px; margin-top: 20px;"></p>
  </div>
  <script>
    const btn = document.getElementById("mic-btn");
    const result = document.getElementById("result");

    const recognition = new webkitSpeechRecognition() || new SpeechRecognition();
    recognition.lang = "he-IL";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    btn.onclick = () => {
      result.textContent = "🎙️ Listening...";
      recognition.start();
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      result.textContent = transcript;

      const streamlitMsg = { transcript: transcript };
      Streamlit.setComponentValue(streamlitMsg);
    };
  </script>
`;

const body = document.getElementsByTagName("body")[0];
body.innerHTML = html;
