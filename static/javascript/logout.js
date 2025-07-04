function logoutUser() {
  fetch("/logout", {
    method: "POST",
    headers: {
      "Authorization": "Bearer " + localStorage.getItem("token"),
    },
  })
    .then((res) => res.json())
    .then((data) => {
      console.log(data.message);
      localStorage.removeItem("token"); 
      window.location.href = "/login";
    })
    .catch((err) => {
      console.error("Logout error:", err);
      localStorage.removeItem("token"); 
      window.location.href = "/login";
    });
}
