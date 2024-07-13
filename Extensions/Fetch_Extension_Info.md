---
layout: default
title: Python
---
Fetch all Extension Info
```js
chrome.management.getAll(function(extensions) {
  var extensionInfo = extensions.map(function(ext) {
    return {
      "Name": ext.name,
      "ID": ext.id,
      "Enabled": ext.enabled ? "Yes" : "No",
      "Version": ext.version,
      "Description": ext.description,
      "Homepage URL": ext.homepageUrl || "Not specified",
      "Options URL": ext.optionsUrl || "Not specified",
      "Permissions": ext.permissions.length > 0 ? ext.permissions.join(', ') : 'None',
      "Type": ext.type,
      "Install Type": ext.installType,
      "May Disable": ext.mayDisable ? "Yes" : "No",
      "May Enable": ext.mayEnable ? "Yes" : "No",
      "Icons": ext.icons.map(function(icon) {
        return {
          "Size": icon.size,
          "URL": icon.url
        };
      }),
      "Host Permissions": ext.hostPermissions.length > 0 ? ext.hostPermissions.join(', ') : 'None',
      "Update URL": ext.updateUrl || "Not specified",
      "Offline Enabled": ext.offlineEnabled ? "Yes" : "No",
      "Is App": ext.isApp ? "Yes" : "No",
      "Disabled Reason": ext.disabledReason || "Not disabled"
    };
  });

  console.log(extensionInfo);
});
```
