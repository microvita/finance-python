function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

let clrbtn = document.getElementById("clrbtn");
clrbtn.addEventListener("click", function (e) {
  let addtxt = document.getElementById("addtext");
  addtxt.value = "";
});
