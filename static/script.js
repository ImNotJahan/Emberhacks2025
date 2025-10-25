document.getElementById("Btn_input").addEventListener("click", async () => {
  const input = document.getElementById("input").value;

  // send to Flask backend via POST
  const response = await fetch("/send", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: input })
  });

  // get JSON reply
  const data = await response.json();

  // show result
  document.getElementById("responseText").textContent = data.message;
});