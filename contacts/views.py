from django.http import HttpResponse, QueryDict
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from .forms import ContactForm
from .models import Contact


@require_GET
def contact_list(request):
    return render(request, "contacts/index.html", {
        "contacts": Contact.objects.all(), "form": ContactForm(),
    })


@require_POST
def contact_add(request):
    form = ContactForm(request.POST)
    if not form.is_valid():
        return render(request, "contacts/_add_errors.html", {"form": form}, status=422)
    contact = form.save()
    return render(request, "contacts/_contact_added.html", {"contact": contact})


@require_GET
def contact_search(request):
    query = request.GET.get("q", "").strip()
    contacts = Contact.objects.filter(name__icontains=query)
    return render(request, "contacts/_contact_rows.html", {"contacts": contacts})


@require_http_methods(["DELETE"])
def contact_delete(request, pk):
    get_object_or_404(Contact, pk=pk).delete()
    # HTMX swaps a 200 response with an empty body; 204 would keep the row.
    return HttpResponse("")


@require_GET
def contact_edit(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    return render(request, "contacts/_contact_edit_row.html", {
        "contact": contact, "form": ContactForm(instance=contact),
    })


@require_GET
def contact_row(request, pk):
    return render(request, "contacts/_contact_row.html", {
        "contact": get_object_or_404(Contact, pk=pk),
    })


@require_http_methods(["PUT"])
def contact_update(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    form = ContactForm(QueryDict(request.body, encoding=request.encoding or "utf-8"), instance=contact)
    if not form.is_valid():
        return render(request, "contacts/_contact_edit_row.html", {
            "contact": contact, "form": form,
        }, status=422)
    return render(request, "contacts/_contact_row.html", {"contact": form.save()})
