function openAffiche(image, title) {
  document.getElementById('lb-modal').style.display = 'flex';
  document.getElementById('lb-img').src = image;
  document.getElementById('lb-title').innerText = title;
}

function closeLb() {
  document.getElementById('lb-modal').style.display = 'none';
}

function openZencard() {
  document.getElementById('zencard-modal').style.display = 'flex';
}

function closeZencard() {
  document.getElementById('zencard-modal').style.display = 'none';
}
