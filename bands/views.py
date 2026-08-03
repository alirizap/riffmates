from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from bands.models import Musician, Band, Venue


def musician(request, musician_id):
    musician = get_object_or_404(Musician, id=musician_id)
    data = {"musician": musician}

    return render(request, "musician.html", data)


def musicians(request):
    all_musicians = Musician.objects.all().order_by("last_name")

    per_page = request.GET.get("per_page", 3)
    try:
        per_page = int(per_page)
    except TypeError, ValueError:
        per_page = 3

    if per_page < 1:
        per_page = 1
    elif per_page > 20:
        per_page = 20

    paginator = Paginator(all_musicians, per_page)

    page_num = request.GET.get("page", 1)
    try:
        page_num = int(page_num)
    except TypeError, ValueError:
        page_num = 1

    if page_num < 1:
        page_num = 1
    elif page_num > paginator.num_pages:
        page_num = paginator.num_pages

    page = paginator.page(page_num)
    data = {"musicians": page.object_list, "page": page}

    return render(request, "musicians.html", data)


def band(request, band_id):
    band = get_object_or_404(Band, id=band_id)
    data = {"band": band}
    return render(request, "band.html", data)


def bands(request):
    all_bands = Band.objects.all().order_by("name")

    per_page = request.GET.get("per_page", 3)
    try:
        per_page = int(per_page)
    except TypeError, ValueError:
        per_page = 3

    if per_page < 1:
        per_page = 1
    elif per_page > 20:
        per_page = 20

    paginator = Paginator(all_bands, per_page)

    page_num = request.GET.get("page", 1)
    try:
        page_num = int(page_num)
    except TypeError, ValueError:
        page_num = 1

    if page_num < 1:
        page_num = 1
    elif page_num > paginator.num_pages:
        page_num = paginator.num_pages

    page = paginator.page(page_num)
    data = {"bands": page.object_list, "page": page}

    return render(request, "bands.html", data)


def venues(request):
    all_venues = Venue.objects.all()
    per_page = request.GET.get("per_page", 3)
    try:
        per_page = int(per_page)
    except TypeError, ValueError:
        per_page = 3

    if per_page < 1:
        per_page = 1
    elif per_page > 20:
        per_page = 20

    paginator = Paginator(all_venues, per_page)

    page_num = request.GET.get("page", 1)
    try:
        page_num = int(page_num)
    except TypeError, ValueError:
        page_num = 1

    if page_num < 1:
        page_num = 1
    elif page_num > paginator.num_pages:
        page_num = paginator.num_pages

    page = paginator.page(page_num)
    data = {"venues": page.object_list, "page": page}

    return render(request, "venues.html", data)


@login_required
def restricted_page(request):
    data = {"title": "Restricted Page", "content": "<h1>You are logged in</h1>"}

    return render(request, "general.html", data)


@login_required
def musician_restricted(request, musician_id):
    musician = get_object_or_404(Musician, musician_id)
    profile = request.user.userprofile
    allowed = False

    if profile.musician_profiles.filter(id=musician_id).exists():
        allowed = True
    else:
        musician_profiles = set(profile.musician_profiles.all())
        for band in musician.band_set.all():
            band_musicians = set(band.musicians.all())
            if musician_profiles.intersection(band_musicians):
                allowed = True
                break

    if not allowed:
        raise Http404("Permission denied")

    content = f"<h1>Musician Page: {musician.last_name}</h1>"
    data = {"title": "Musician Restricted", "content": content}

    return render(request, "general.html", data)
