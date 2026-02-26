// signup.js

document.addEventListener("DOMContentLoaded", function() {
    const signupForm = document.querySelector("form");

    signupForm.addEventListener("submit", function(event) {
        const fname = document.querySelector("input[name='fname']").value;
        const lname = document.querySelector("input[name='lname']").value;
        const uname = document.querySelector("input[name='uname']").value;
        const pwd = document.querySelector("input[name='pwd']").value;
        const email = document.querySelector("input[name='email']").value;
        const contact = document.querySelector("input[name='contact']").value;
        const dob = document.querySelector("input[name='dob']").value;
        const address = document.querySelector("textarea[name='add']").value;
        const userType = document.querySelector("input[name='reg']:checked");
        const termsAccepted = document.querySelector("input[name='chkChecked']").checked;

        if (!fname || !lname || !uname || !pwd || !email || !contact || !dob || !address || !userType || !termsAccepted) {
            alert("Please fill in all required fields and accept the terms and conditions.");
            event.preventDefault();
            return;
        }

        // Additional validation can be added here
    });
});