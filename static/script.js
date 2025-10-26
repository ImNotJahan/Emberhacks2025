const console_txt = document.getElementById("console");
const responses   = document.getElementById("responses");

document.getElementById("Btn_input").addEventListener("click", async () => {
  const input = document.getElementById("input").value;
  isWaiting = false

  document.getElementById("console").innerHTML = "Calculating...";
  console_txt.style.color = "black";
  
  //Sends the input
  const response = await fetch("/getInput", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: input })
  });
  const data = await response.json();

  if(data.failed) {
    responses.style.display = "none";
    console_txt.innerHTML   = data.console;
    console_txt.style.color = "red"
    return;
  } else {
    responses.style.display = "block";
  }

  document.getElementById("sol").innerHTML = data.sol;//Prints out the values
  document.getElementById("equ").innerHTML = data.equ;//Prints out the values
  document.getElementById("val").innerHTML = data.val;//Prints out the values
  document.getElementById("console").innerHTML = data.console;//Prints out the values
  console.log(data)
});