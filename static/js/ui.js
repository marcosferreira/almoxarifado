// Centralized UI helpers for the application
document.addEventListener('DOMContentLoaded', function () {
  // global keyboard shortcuts mapping (delegates to elements that expose dataset.shortcut)
  window.addEventListener('keydown', function (e) {
    // ignore if typing in an input or textarea
    const tag = document.activeElement && document.activeElement.tagName;
    if (tag === 'INPUT' || tag === 'TEXTAREA' || document.activeElement.isContentEditable) return;

    // map keys to events
    switch (e.key) {
      case 'F2':
        document.dispatchEvent(new CustomEvent('ui:shortcut', {detail: 'F2'}));
        break;
      case 'F3':
        document.dispatchEvent(new CustomEvent('ui:shortcut', {detail: 'F3'}));
        break;
      case 'F5':
        document.dispatchEvent(new CustomEvent('ui:shortcut', {detail: 'F5'}));
        break;
      case 'F7':
        document.dispatchEvent(new CustomEvent('ui:shortcut', {detail: 'F7'}));
        break;
      case 'Escape':
        document.dispatchEvent(new CustomEvent('ui:shortcut', {detail: 'Escape'}));
        break;
    }
  });
});
