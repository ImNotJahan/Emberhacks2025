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
//document.getElementById("Btn_sighn").addEventListener("click", async () => {
  
//});