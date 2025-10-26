document.getElementById("Btn_input").addEventListener("click", async () => {
  const input = document.getElementById("input").value;
  
  //Sends the input
  const response = await fetch("/getInput", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: input })
  });
  const data = await response.json();
  document.getElementById("sol").textContent = data.sol;//Prints out the values
  document.getElementById("equ").textContent = data.equ;//Prints out the values
  document.getElementById("val").textContent = data.val;//Prints out the values
  console.log(data)
});