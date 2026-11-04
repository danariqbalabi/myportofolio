// Keep HTTP 422 as a failed request, but display the server's validation errors.
document.body.addEventListener('htmx:beforeSwap', function (event) {
  if (event.detail.xhr.status !== 422) return;
  event.detail.shouldSwap = true;
  if (event.detail.requestConfig.elt.id === 'add-contact-form') {
    event.detail.target = document.getElementById('feedback');
    event.detail.swapOverride = 'outerHTML';
  }
});

document.getElementById('add-contact-form').addEventListener('htmx:afterRequest', function (event) {
  if (!event.detail.successful) return;
  this.reset();
  // Reconcile the table if a contact was added while a search was active.
  const search = document.getElementById('contact-search');
  if (search.value) {
    search.value = '';
    htmx.trigger(search, 'search');
  }
});

function showRequestError(event) {
  if (event.detail.xhr && event.detail.xhr.status === 422) return;
  document.getElementById('feedback').textContent = 'Permintaan gagal. Silakan coba lagi.';
}
document.body.addEventListener('htmx:responseError', showRequestError);
document.body.addEventListener('htmx:sendError', showRequestError);
