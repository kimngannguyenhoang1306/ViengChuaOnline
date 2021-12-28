# encoding: utf-8
from django.conf import settings
from django.core.paginator import InvalidPage, Paginator
from django.http import Http404
from django.shortcuts import render
import json
from django.http import JsonResponse
from haystack.forms import FacetedSearchForm, ModelSearchForm
from haystack.query import EmptySearchQuerySet

RESULTS_PER_PAGE = getattr(settings, "HAYSTACK_SEARCH_RESULTS_PER_PAGE", 20)


class SearchView(object):
    template = "ViengChua/Search.html"
    extra_context = {}
    query = ""
    results = EmptySearchQuerySet()
    request = None
    searchform = None
    results_per_page = RESULTS_PER_PAGE

    def __init__(
        self,
        template=None,
        load_all=True,
        searchform_class=None,
        searchqueryset=None,
        results_per_page=None,
    ):
        self.load_all = load_all
        self.searchform_class = searchform_class
        self.searchqueryset = searchqueryset

        if searchform_class is None:
            self.searchform_class = ModelSearchForm

        if results_per_page is not None:
            self.results_per_page = results_per_page

        if template:
            self.template = template

    def __call__(self, request):
        """
        Generates the actual response to the search.

        Relies on internal, overridable methods to construct the response.
        """
        self.request = request

        self.searchform = self.build_searchform()
        self.query = self.get_query()
        self.results = self.get_results()

        return self.create_response()

    def build_searchform(self, searchform_kwargs=None):
        """
        Instantiates the searchform the class should use to process the search query.
        """
        data = None
        kwargs = {"load_all": self.load_all}
        if searchform_kwargs:
            kwargs.update(searchform_kwargs)

        if len(self.request.GET):
            data = self.request.GET

        if self.searchqueryset is not None:
            kwargs["searchqueryset"] = self.searchqueryset

        return self.searchform_class(data, **kwargs)

    def get_query(self):
        """
        Returns the query provided by the user.

        Returns an empty string if the query is invalid.
        """
        if self.searchform.is_valid():
            return self.searchform.cleaned_data["q"]

        return ""

    def get_results(self):
        """
        Fetches the results via the searchform.

        Returns an empty list if there's no query to search with.
        """
        return self.searchform.search()

    def build_page(self):
        """
        Paginates the results appropriately.

        In case someone does not want to use Django's built-in pagination, it
        should be a simple matter to override this method to do what they would
        like.
        """
        try:
            page_no = int(self.request.GET.get("page", 1))
        except (TypeError, ValueError):
            raise Http404("Not a valid number for page.")

        if page_no < 1:
            raise Http404("Pages should be 1 or greater.")

        start_offset = (page_no - 1) * self.results_per_page
        self.results[start_offset : start_offset + self.results_per_page]

        paginator = Paginator(self.results, self.results_per_page)

        try:
            page = paginator.page(page_no)
        except InvalidPage:
            raise Http404("No such page!")

        return (paginator, page)

    def extra_context(self):
        """
        Allows the addition of more context variables as needed.

        Must return a dictionary.
        """
        return {}

    def get_context(self):
        (paginator, page) = self.build_page()

        context = {
            "query": self.query,
            "searchform": self.searchform,
            "page": page,
            "paginator": paginator,
            "suggestion": None,
        }

        if (
            hasattr(self.results, "query")
            and self.results.query.backend.include_spelling
        ):
            context["suggestion"] = self.searchform.get_suggestion()

        context.update(self.extra_context())

        return context

    def create_response(self):
        """
        Generates the actual HttpResponse to send back to the user.
        """

        context = self.get_context()

        return render(self.request, self.template, context)


def search_view_factory(view_class=SearchView, *args, **kwargs):
    def search_view(request):
        return view_class(*args, **kwargs)(request)

    return search_view


class FacetedSearchView(SearchView):
    def __init__(self, *args, **kwargs):
        # Needed to switch out the default searchform class.
        if kwargs.get("searchform_class") is None:
            kwargs["searchform_class"] = FacetedSearchsearchform

        super(FacetedSearchView, self).__init__(*args, **kwargs)

    def build_searchform(self, searchform_kwargs=None):
        if searchform_kwargs is None:
            searchform_kwargs = {}

        # This way the searchform can always receive a list containing zero or more
        # facet expressions:
        searchform_kwargs["selected_facets"] = self.request.GET.getlist("selected_facets")

        return super(FacetedSearchView, self).build_searchform(searchform_kwargs)

    def extra_context(self):
        extra = super(FacetedSearchView, self).extra_context()
        extra["request"] = self.request
        extra["facets"] = self.results.facet_counts()
        return extra


def basic_search(
    request,
    template="ViengChua/MainPage.html",
    load_all=True,
    searchform_class=ModelSearchForm,
    searchqueryset=None,
    extra_context=None,
    results_per_page=None,
):
    """
    A more traditional view that also demonstrate an alternative
    way to use Haystack.

    Useful as an example of for basing heavily custom views off of.

    Also has the benefit of thread-safety, which the ``SearchView`` class may
    not be.

    Template:: ``search/search.html``
    Context::
        * searchform
          An instance of the ``searchform_class``. (default: ``ModelSearchsearchform``)
        * page
          The current page of search results.
        * paginator
          A paginator instance for the results.
        * query
          The query received by the searchform.
    """
    query = ""
    results = EmptySearchQuerySet()

    if request.GET.get("q"):
        searchform = searchform_class(request.GET, searchqueryset=searchqueryset, load_all=load_all)

        if searchform.is_valid():
            query = searchform.cleaned_data["q"]
            results = searchform.search()
    else:
        searchform = searchform_class(searchqueryset=searchqueryset, load_all=load_all)

    paginator = Paginator(results, results_per_page or RESULTS_PER_PAGE)

    try:
        page = paginator.page(int(request.GET.get("page", 1)))
    except InvalidPage:
        raise Http404("No such page of results!")

    context = {
        "searchform": searchform,
        "page": page,
        "paginator": paginator,
        "query": query,
        "suggestion": None,
    }

    if results.query.backend.include_spelling:
        context["suggestion"] = searchform.get_suggestion()

    if extra_context:
        context.update(extra_context)

    return render(request, template, context)
