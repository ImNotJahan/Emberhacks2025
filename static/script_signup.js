document.getElementById("btn_sign_up").addEventListener("click", async () => {
  const user = document.getElementById("user_s").value;
  const password = document.getElementById("password_s").value;
  const response = await fetch("/verify-signup", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username: user, password:  password})
  });
  const data = await response.json();

});