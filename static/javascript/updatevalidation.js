async function submitLogin(event) {

    event.preventDefault(); 

    const name = document.getElementById("name").value;
    const age = document.getElementById("age").value;
    const dob = document.getElementById("dob").value;
    const email = document.getElementById("email").value;
    const contact = document.getElementById("contact").value;
    
    const errorMsg = document.getElementById("error");

    errorMsg.innerText = ""; 

    $.ajax({
    url: '/update',
    method: 'POST',
    contentType: "application/json",
    data: JSON.stringify({name, age, dob, email, contact}),
    headers: {
        "Authorization": "Bearer " + localStorage.getItem("token") 
    },
    success: function(res){
        window.location.href ='/';
    },
    error: function(xhr){
        const res = xhr.responseJSON;
        errorMsg.innerText = res?.message || "Something went wrong!";
    }
})

}
