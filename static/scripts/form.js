const webSocketForm = document.getElementById("webSocketForm");
const addUrlButton = document.getElementById("addUrlButton");
const urlContainer = document.getElementById("urlContainer");

addUrlButton.addEventListener("click", function () {
  const input = document.createElement("input");
  input.type = "text";
  input.placeholder = "Enter WebSocket URL";
  input.className = "webSocketURL border rounded py-2 px-4 mb-2";
  urlContainer.appendChild(input);
});

webSocketForm.addEventListener("submit", function (event) {
  event.preventDefault();
  const webSocketURLs = Array.from(
    document.querySelectorAll(".webSocketURL")
  ).map((input) => input.value);

  fetch("http://localhost:8080/submit_url", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ urls: webSocketURLs }),
  })
    .then((response) => {
      if (response.ok) {
        console.log("WebSocket URLs sent successfully");
        // 必要に応じて、接続成功時の処理をここに追加
      } else {
        console.error("Failed to send WebSocket URLs");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});
