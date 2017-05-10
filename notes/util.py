import re

from django.db.models import Q


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def build_query(query_string, search_fields):
    """ Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    """
    query = None  # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None  # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})

            if or_query:
                or_query = or_query | q
            else:
                or_query = q

        if query:
            query = query & or_query
        else:
            query = or_query
    return query


def generic_search(fields, query, queryset):
    entry_query = build_query(query, fields)
    print(entry_query)
    found_entries = queryset.filter(entry_query)
    return found_entries


def isNotBlank(my_string):
    if my_string and my_string.strip():
        # my_string is not None AND my_string is not empty or blank
        return True
    # my_string is None OR my_string is empty or blank
    return False
