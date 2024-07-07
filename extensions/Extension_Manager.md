Extension Manager
```js
chrome.management.getAll(function(extensions) {
  var options = [];
  extensions.forEach(function(extension) {
    if (extension.id !== chrome.runtime.id) {
      options.push(extension.name);
    }
  });
  var choice = prompt("Choose an extension to manage:\\n" + options.join("\\n"));
  var selectedExtension = extensions.find(function(ext) {
    return ext.name === choice;
  });
  if (selectedExtension) {
    var action = selectedExtension.enabled ? 'disable' : 'enable';
    var confirmAction = confirm('Do you want to ' + action + ' the extension: ' + selectedExtension.name + '?');
    if (confirmAction) {
      chrome.management.setEnabled(selectedExtension.id, !selectedExtension.enabled, function() {
        if (chrome.runtime.lastError) {
          console.error('Failed to ' + action + ' extension ' + selectedExtension.name + ': ' + chrome.runtime.lastError.message);
        } else {
          refreshExtensionList();
          openWebStore();
        }
      });
    }
  } else {
    alert('Invalid choice');
  }
});
```
