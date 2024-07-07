chrome.management.getAll(function(extensions) {
  extensionList.innerHTML = '';
  extensions.forEach(function(extension) {
    if (extension.id !== chrome.runtime.id) {
      var p = document.createElement('p');
      p.textContent = extension.name;
      extensionList.appendChild(p);
    }
  });
});
