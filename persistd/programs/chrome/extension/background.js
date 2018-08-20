// Example URL to test stuff:
// http://idontthinkthis.domainwilleverexist?project_name=proh_joo&action=start

// Launches the tabs associated with a project and saved the windowId
function launchTabs(project) {
    project = project[projectName];
    if(project && project.tabs) {
        for(i=0; i < project.tabs.length; i++) {
            tabUrl = project.tabs[i];
            if(i==0) {
                chrome.tabs.update(tabId, { url: tabUrl}, function(tab) { console.log('Successfully updated'); });
            } else {
                chrome.tabs.create({
                    windowId: windowId,
                    url: tabUrl
                }, function(tab) { console.log('Created tab for: ' + tab.url)});
            }
        }
    } else {
        chrome.tabs.update(tabId, { url: 'https:///www.google.com/'}, function(tab) { console.log('Successfully updated'); });
    }
    obj = {};
    newProjectObject = {windowId: windowId};
    if(project && project.tabs) {
        newProjectObject['tabs'] = project.tabs;
    }
    obj[projectName] = newProjectObject;
    chrome.storage.local.set(obj, function() { console.log('Saved windowId'); });
}

// Starts a new instance of this program
function start(windowId) {
    console.log('start called');
    chrome.storage.local.get(projectName, launchTabs)
}

// Saves the tabs, closes the triggering tab, and closes the window
function saveTabsAndClose(tabs) {
    tabUrls = []
    for(i in tabs) {
        tab = tabs[i];
        if(tab.url && !tab.url.startsWith('http://idontthinkthis.domainwilleverexist')) {
            tabUrls.push(tab.url);
            console.log('Saved tab: ' + tab.url);
        }
    }
    obj = {};
    obj[projectName] = {tabs: tabUrls};
    chrome.storage.local.set(obj, function() { console.log('Saved tabs'); });
    // first, close the opened tab that triggered this script
    chrome.tabs.remove(tabId, function() { console.log('Removed triggering tab'); });
    // then, close the window
    chrome.windows.remove(savedWindowId, function() { console.log('Closed window'); });
    if(destroy) {
        chrome.storage.local.remove(projectName, function() { console.log('Removed project: ' + projectName); });
    }
}

// Gets the saved window from project storage
// and then calls saveTabsAndClose()
function getSavedWindow(project) {
    project = project[projectName];
    if(project && project.windowId != undefined) {
        savedWindowId = project.windowId;
        chrome.tabs.query({windowId: savedWindowId}, saveTabsAndClose);
    } else {
        chrome.tabs.remove(tabId, function() { console.log('Removed triggering tab'); });
        console.log("Can't find any window id for this project");
    }
}

// Closes the program, persisting the state
function close(windowId) {
    console.log('close called');
    chrome.storage.local.get(projectName, getSavedWindow);
}

// Launch an action based on the action variable
function launchAction(tab) {
    windowId = tab.windowId;
    switch(action) {
        case 'start':
            start(windowId);
            break;
        case 'close':
            // Just close, don't destroy the storage
            close(windowId);
            destroy = false;
            break;
        case 'destroy':
            // Same as above, but do destroy the storage
            close(windowId);
            destroy = true;
            break;
        default:
            console.log("not a valid action.")
            return;
    }
};

// Add a listener for this specific address
chrome.webRequest.onBeforeRequest.addListener(
    function(details) {
        matches = details.url.match("project_name=([^&]*)&action=([^&]*)");
        projectName = matches[1]
        action = matches[2]
        tabId = details.tabId;
        chrome.tabs.get(tabId, launchAction);
        return { cancel: true };
    },
    {
        urls: ["*://idontthinkthis.domainwilleverexist/*"]
    },
    ["blocking"]
);
