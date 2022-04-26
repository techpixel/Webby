var markdownUpdate = document.getElementById('markdown');
var outputHTML = document.getElementById('content');

function update() {
  newHtml = sanitizeHtml(marked(markdownUpdate.value, { breaks: true }), {
  allowedTags: sanitizeHtml.defaults.allowedTags.concat([ 'img', 'h1', 'h2' ])
  });
  outputHTML.innerHTML = newHtml;
}

if (markdownUpdate) { 
  markdownUpdate.addEventListener("input", update);
}