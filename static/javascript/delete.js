function deleteProfile() {
    const confirmed = confirm("Are you sure you want to delete your profile? This action cannot be undone.");

    if (!confirmed) return;

    $.ajax({
        url: "/delete",
        method: "POST",
        headers: {
            "Authorization": "Bearer " + localStorage.getItem("token")
        },
        success: function(data) {
            alert(data.message);
            if (data.status === "success") {
                localStorage.removeItem("token");
                window.location.href = "/login";
            }
        },
        error: function(xhr) {
            console.error("Delete error:", xhr);
            alert("Something went wrong while deleting your profile.");
        }
    });
}
