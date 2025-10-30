const console_txt = document.getElementById("console");
const responses   = document.getElementById("responses");
const text_input  = document.getElementById("input");

document.getElementById("Btn_input").addEventListener("click", async () => {
  console_txt.innerHTML = "Calculating...";
  console_txt.style.color = "black";

    //Sends the input
    const response = await fetch("/getInput", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: text_input.value })
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

  document.getElementById("sol").innerHTML     = data.sol; // display sequential solution
  document.getElementById("equ").innerHTML     = data.equ; // display composite solution
  document.getElementById("val").innerHTML     = data.val; // display result
  document.getElementById("console").innerHTML = data.console; // update console
});