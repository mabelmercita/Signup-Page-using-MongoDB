function display() {

    let uname = document.getElementById("name").value;
    let pwd = document.getElementById("password").value;
    let cpwd = document.getElementById("confpassword").value;
    let mail = document.getElementById("mail").value;

    if (!errormessage(uname, pwd)) {
        return false;
    }

    if (pwd !== cpwd) {
        error.innerHTML = "<span style='color: red;'>Passwords do not match.</span>"; 
        return false;
    }

    console.log("Username:", uname);
    console.log("Password:", pwd);
    console.log("Email:", mail);

    return true;
}


function errormessage(uname, pwd) {

    let error = document.getElementById("error");

    let pwdregex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@.#$!%*?&])[A-Za-z\d@.#$!%*?&]{8,15}$/;
    let nameregex = /^[A-Za-z\s]+$/;

    if (!pwdregex.test(pwd)) {
        error.innerHTML = "<span style='color: red;'>Password must have 1 uppercase, 1 lowercase, 1 digit, 1 special char, and be 8-15 chars long.</span>";
        return false;
    }

    if (!nameregex.test(uname)) {
        error.innerHTML = "<span style='color: red;'>Name should only contain alphabets and spaces.</span>";
        return false;
    }


    error.innerHTML = ""; 
    return true;
}

