// Background script
// Not strictly needed for this simple flow but good for persistence
chrome.runtime.onInstalled.addListener(() => {
  console.log("AI Translator Extension Installed");
});
