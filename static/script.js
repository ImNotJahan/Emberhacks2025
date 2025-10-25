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

  //Sends the input
  const response = await fetch("/getInput", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: input , isFull: checked})
  });
  
  document.getElementById("responseText").textContent = data.message;//Prints out the values
  const box = document.getElementById("darkMode");
});