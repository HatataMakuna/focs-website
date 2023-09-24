document.addEventListener("DOMContentLoaded", function () {
  const loginBtn = document.getElementById("loginBtn");
  const loginStatus = document.getElementById("login-status");

  loginBtn.addEventListener("click", function (e) {
      e.preventDefault();

      // Get the values from the input fields
      const username = document.getElementById("username").value;
      const password = document.getElementById("password").value;

      // Send login data to the server for authentication
      fetch("/path/to/your/login_script.php", {
          method: "POST",
          body: JSON.stringify({ username, password }),
          headers: {
              "Content-Type": "application/json"
          }
      })
      .then(response => response.json())
      .then(data => {
          if (data.success) {
              // Authentication successful
              loginStatus.innerHTML = "Login successful! Welcome, " + data.username;
          } else {
              // Authentication failed
              loginStatus.innerHTML = "Login failed. Please check your credentials.";
          }
      })
      .catch(error => {
          console.error("Error authenticating:", error);
      });
  });
});
