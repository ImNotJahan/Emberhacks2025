document.getElementById("btn_login").addEventListener("click", async () => {
  const user = document.getElementById("user_l").value;
  const password = document.getElementById("password_l").value;
  const response = await fetch("/verifylogin", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username: user, password:  password})
  });
  const data = await response.json();

});
//
//document.getElementById("btn_sign_in").addEventListener("click", async () => {
//  const user = document.getElementById("user_s").value;
//  const password = document.getElementById("password_s").value;
//  const response = await fetch("/signin", {
//    method: "POST",
//    headers: { "Content-Type": "application/json" },
//    body: JSON.stringify({ username: user, password:  password})
//  });
//  const data = await response.json();
//
//});