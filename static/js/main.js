
const onFileChanged = () => {;
    console.log("On file changed");
    const uploadPathText = $(".custom-file-input").val();
    console.log(uploadPathText);
    const uploadName = uploadPathText.split("\\").slice(-1);
    console.log("uplaod name " + uploadName);
    $(".custom-file-label").text(uploadName);
}

$(document).ready(() => {
    console.log("Using jquery");


});
