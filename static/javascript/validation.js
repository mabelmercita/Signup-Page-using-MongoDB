async function submitLogin(event) {

    event.preventDefault(); 

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    
    const errorMsg = document.getElementById("error");

    errorMsg.innerText = ""; 

    const response = await fetch("/login", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({ username, password })
    });

    const result = await response.json();
    console.log(result);


    if (result.status === "success") {
        window.location.href = "/"; 
    } else {
        errorMsg.innerText = result.message;
    }
}
