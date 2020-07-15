from django.conf.urls import include, url

from API.publication.views.publication import (NewPublications,
                                               PublicationAutocomplete,
                                               PublicationDetail, Publications,
                                               PublicationSearch,
                                               RelatedContent)

urlpatterns = [
    url(r'^publication$', Publications.as_view()),  # ?max_results=XXX&offset=YYY&type=ZZZ
    url(r'^new_publications$', NewPublications.as_view()),
    url(r'^pub_details/(?P<slug>[\w-]+)$', PublicationDetail.as_view()),
    url(r'^related_content/(?P<amount>[\w-]+)$', RelatedContent.as_view()),
    url(r'^publication_search', PublicationSearch.as_view()),
    url(r'^froala_editor/', include('froala_editor.urls')),
    url(r'^autocomplete_publication$', PublicationAutocomplete.as_view()),
]
