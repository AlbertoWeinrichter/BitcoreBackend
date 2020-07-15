from django.conf.urls import url

from API.general.views.general import (AcceptManifesto, ContactForm, FixDB,
                                       PublicityView, QuoteView,
                                       TagAutocomplete, TagDetailView)

urlpatterns = [
    url(r'^quote$', QuoteView.as_view()),
    url(r'^tag_detail$', TagDetailView.as_view()),
    url(r'^publicity/(?P<ad_type>[\w-]+)$', PublicityView.as_view()),
    url(r'^accept_manifesto$', AcceptManifesto.as_view()),
    url(r'^contact_form$', ContactForm.as_view()),
    url(r'^autocomplete_tag$', TagAutocomplete.as_view()),
    url(r'^fix_db$', FixDB.as_view()),
]
