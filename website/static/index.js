function deleteNote(inviteId) {
  fetch("/delete-invite", {
    method: "POST",
    body: JSON.stringify({ inviteId: inviteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}
