async function askAI() {
  const url = document.getElementById("url").value.trim();
  const question = document.getElementById("question").value.trim();
  const answerBox = document.getElementById("answer");

  if (!url || !question) {
    answerBox.innerText = "⚠️ Please enter both website URL and question.";
    return;
  }

  answerBox.innerText = "🤖 Gemini is analyzing the website...";

  try {
    const response = await fetch("http://127.0.0.1:5000/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        url: url,
        question: question
      })
    });

    const data = await response.json();
    answerBox.innerText = data.answer || "No response from AI.";

  } catch (error) {
    answerBox.innerText =
      "❌ Unable to connect to backend. Please run Flask server.";
  }
}
