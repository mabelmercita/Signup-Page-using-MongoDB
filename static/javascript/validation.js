async function submitLogin(event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const errorMsg = document.getElementById("error");
    errorMsg.innerText = "";

    $.ajax({
        url: "/login",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({ username, password }),

        success: function (res) {
            if (res.status === "success") {
            
                localStorage.setItem("token", res.access_token);

                window.location.href = "/?token=" + res.access_token;
            } else {
                errorMsg.innerText = res.message;
            }
        },

        error: function (xhr) {
            const res = xhr.responseJSON;
            errorMsg.innerText = res?.message || "Something went wrong!";
        }
    });
}
