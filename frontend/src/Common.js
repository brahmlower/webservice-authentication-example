
function isAuthed() {
  return null !== localStorage.getItem('token');
}

export { isAuthed }
