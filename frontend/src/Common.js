
const linkButtonStyle = { padding: 0, border: 0, verticalAlign: 'top'}

function isAuthed() {
  return null !== localStorage.getItem('token');
}

export { isAuthed, linkButtonStyle }
