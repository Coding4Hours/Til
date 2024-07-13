---
layout: default
title: Python
---
Disable all extensions
```js
chrome.management.getAll(function(extensions) {
  extensions.forEach(function(extension) {
    if (extension.id !== chrome.runtime.id && extension.enabled) {
      chrome.management.setEnabled(extension.id, false);
    }
  });
```
