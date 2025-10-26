document.getElementById("Btn_input").addEventListener("click", async () => {
  const input = document.getElementById("input").value;
  isWaiting = false
  document.getElementById("console").innerHTML = "Waiting!";
  //Sends the input
  const response = await fetch("/getInput", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: input })
  });
  const data = await response.json();

  if(data.failed) {
    document.getElementById("responses").style.display = "none";
    document.getElementById("console").innerHTML = data.console;
    return;
  } else {
    document.getElementById("responses").style.display = "block";
  }

  document.getElementById("sol").innerHTML = data.sol;//Prints out the values
  document.getElementById("equ").innerHTML = data.equ;//Prints out the values
  document.getElementById("val").innerHTML = data.val;//Prints out the values
  document.getElementById("console").innerHTML = data.console;//Prints out the values
  console.log(data)
});
document.getElementById("Btn_login").addEventListener("click", async () => {
  const user = document.getElementById("user_l").value;
  const password = document.getElementById("password_l").value;
  const response = await fetch("/verifylogin", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username: user, password:  password})
  });
  const data = await response.json();
  
});
document.getElementById("Btn_sighn").addEventListener("click", async () => {
  
});