const recordBtn = document.getElementById("recordBtn");
const status = document.getElementById("status");
const chatBox = document.getElementById("chatBox");

let mediaRecorder;
let chunks = [];

recordBtn.addEventListener("mousedown", async () => {
  status.innerText = "Recording...";

  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  mediaRecorder = new MediaRecorder(stream);
  mediaRecorder.start();

  chunks = [];

  mediaRecorder.ondataavailable = (e) => {
    chunks.push(e.data);
  };

  mediaRecorder.onstop = async () => {
    status.innerText = "Processing...";

    const blob = new Blob(chunks, { type: "audio/wav" });
    const formData = new FormData();
    formData.append("file", blob);

    const res = await fetch("/transcribe", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();

    // Update chat UI
    if (data.user && data.assistant) {
      chatBox.innerHTML += `<p class="user">👤 ${data.user}</p>`;
      chatBox.innerHTML += `<p class="assistant">🤖 ${data.assistant}</p>`;
      chatBox.scrollTop = chatBox.scrollHeight;
    }

    status.innerText = "Press and hold the button to speak";
  };
});

recordBtn.addEventListener("mouseup", () => {
  if (mediaRecorder && mediaRecorder.state === "recording") {
    mediaRecorder.stop();
  }
});
