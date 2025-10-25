document.getElementById("Btn_input").addEventListener("click", async () => {
  const input = document.getElementById("input").value;
  const fw = document.getElementById("full_work");
  var checked = false;
  if (fw.checked){
    checked =true;
  }
  else{
    checked = false;
  }
  const response = await fetch("/send", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: input , isFull: checked})
  });
  box.addEventListener("change", async () => {
    const payload = { checked: fw.checked };
  });
  document.getElementById("responseText").textContent = data.message;
  const box = document.getElementById("darkMode");
});