import contextlib
from copyreg import add_extension

import pytest

from pyarr.exceptions import PyarrMissingArgument, PyarrResourceNotFound
from pyarr.models.common import PyarrSortDirection
from pyarr.models.radarr import RadarrEventType, RadarrSortKeys

from tests import load_fixture
from tests.conftest import radarr_client


@pytest.mark.usefixtures
def test__movie_json(responses, radarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:7878/api/v3/movie/lookup?term=tmdb%3A123456",
        headers={"Content-Type": "application/json"},
        body=load_fixture("radarr/movie_lookup.json"),
        status=200,
        match_querystring=True,
    )

    data = radarr_client._movie_json(
        id_=123456,
        quality_profile_id=1,
        root_dir="/",
        monitored=False,
        search_for_movie=False,
    )

    assert isinstance(data, dict)
    assert data["title"] == "string"
    assert data["rootFolderPath"] == "/"
    assert data["qualityProfileId"] == 1
    assert data["year"] == 2014
    assert data["tmdbId"] == 123456
    assert isinstance(data["images"], list)
    assert data["titleSlug"] == "123456"
    assert data["monitored"] == False
    assert data["addOptions"]["searchForMovie"] == False


@pytest.mark.usefixtures
def test_get_movie(responses, radarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:7878/api/v3/movie",
        headers={"Content-Type": "application/json"},
        body=load_fixture("radarr/movie_all.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_client.get_movie()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:7878/api/v3/movie/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("radarr/movie.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_client.get_movie(id_=1)
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:7878/api/v3/movie?tmdbid=123456",
        headers={"Content-Type": "application/json"},
        body=load_fixture("radarr/movie_tmdb.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_client.get_movie(id_=123456, tmdb=True)
    assert isinstance(data, list)


# TODO: add_movie
# TODO: upd_movie


@pytest.mark.usefixtures
def test_get_movie_by_movie_id(responses, radarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:7878/api/v3/movie/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("radarr/movie.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_client.get_movie_by_movie_id(1)

    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:7878/api/v3/movie/999",
        headers={"Content-Type": "application/json"},
        status=404,
        match_querystring=True,
    )
    with contextlib.suppress(PyarrResourceNotFound):
        data = radarr_client.get_movie_by_movie_id(999)
        assert False


# TODO: del_movie
@pytest.mark.usefixtures
def test_del_movie(responses, radarr_client):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:7878/api/v3/movie/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/delete.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_client.del_movie(1)
    assert isinstance(data, dict)

    responses.add(
        responses.DELETE,
        "https://127.0.0.1:7878/api/v3/movie/1?deleteFiles=True&addImportExclusion=True",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/delete.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_client.del_movie(id_=1, delete_files=True, add_exclusion=True)
    assert isinstance(data, dict)

    responses.add(
        responses.DELETE,
        "https://127.0.0.1:7878/api/v3/movie/999",
        headers={"Content-Type": "application/json"},
        status=404,
    )
    with contextlib.suppress(PyarrResourceNotFound):
        data = radarr_client.del_movie(999)
        assert False

    responses.add(
        responses.DELETE,
        "https://127.0.0.1:7878/api/v3/movie/editor",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/delete.json"),
        status=200,
    )
    data = radarr_client.del_movie(id_=[1, 2, 3])
    assert isinstance(data, dict)

    responses.add(
        responses.DELETE,
        "https://127.0.0.1:7878/api/v3/movie/editor",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/delete.json"),
        status=200,
    )
    data = radarr_client.del_movie(id_=[1, 2, 3], delete_files=True, add_exclusion=True)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_lookup_movie(responses, radarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:7878/api/v3/movie/lookup?term=imdb:123456",
        headers={"Content-Type": "application/json"},
        body=load_fixture("radarr/movie_lookup.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_client.lookup_movie(term="imdb:123456")
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:7878/api/v3/movie/lookup?term=tmdb:123456",
        headers={"Content-Type": "application/json"},
        body=load_fixture("radarr/movie_lookup.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_client.lookup_movie(term="tmdb:123456")
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:7878/api/v3/movie/lookup?term=Movie",
        headers={"Content-Type": "application/json"},
        body=load_fixture("radarr/movie_lookup.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_client.lookup_movie(term="Movie")
    assert isinstance(data, list)


@pytest.mark.usefixtures
def test_lookup_movie_by_tmdb_id(responses, radarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:7878/api/v3/movie/lookup?term=tmdb:123456",
        headers={"Content-Type": "application/json"},
        body=load_fixture("radarr/movie_lookup.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_client.lookup_movie_by_tmdb_id(id_=123456)
    assert isinstance(data, list)


@pytest.mark.usefixtures
def test_lookup_movie_by_imdb_id(responses, radarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:7878/api/v3/movie/lookup?term=imdb:123456",
        headers={"Content-Type": "application/json"},
        body=load_fixture("radarr/movie_lookup.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_client.lookup_movie_by_imdb_id(id_="123456")
    assert isinstance(data, list)


# TODO: upd_movies
@pytest.mark.usefixtures
def test_get_movie_file(responses, radarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:7878/api/v3/moviefile/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("radarr/moviefile.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_client.get_movie_file(id_=1)
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:7878/api/v3/moviefile?movieFileIds=1&movieFileIds=2&movieFileIds=3&movieFileIds=4",
        headers={"Content-Type": "application/json"},
        body=load_fixture("radarr/moviefiles.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_client.get_movie_file(id_=[1, 2, 3, 4])
    assert isinstance(data, list)


# TODO: del_movie
@pytest.mark.usefixtures
def test_del_movie_file(responses, radarr_client):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:7878/api/v3/moviefile/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/delete.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_client.del_movie_file(id_=1)
    assert isinstance(data, dict)

    responses.add(
        responses.DELETE,
        "https://127.0.0.1:7878/api/v3/moviefile/999",
        headers={"Content-Type": "application/json"},
        status=404,
    )
    with contextlib.suppress(PyarrResourceNotFound):
        data = radarr_client.del_movie_file(id_=999)
        assert False

    responses.add(
        responses.DELETE,
        "https://127.0.0.1:7878/api/v3/moviefile/bulk",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/delete.json"),
        status=200,
    )
    data = radarr_client.del_movie_file(id_=[1, 2, 3])
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_get_movie_history(responses, radarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:7878/api/v3/history/movie?movieId=1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("radarr/movie_history.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_client.get_movie_history(id_=1)
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:7878/api/v3/history/movie?movieId=1&eventType=unknown",
        headers={"Content-Type": "application/json"},
        body=load_fixture("radarr/movie_history.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_client.get_movie_history(id_=1, event_type=RadarrEventType.UNKNOWN)
    assert isinstance(data, list)


@pytest.mark.usefixtures
def test_get_blocklist_by_movie_id(responses, radarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:7878/api/v3/blocklist/movie?movieId=1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("radarr/movie_blocklist.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_client.get_blocklist_by_movie_id(id_=1)
    assert isinstance(data, list)


@pytest.mark.usefixtures
def test_get_queue(responses, radarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:7878/api/v3/queue",
        headers={"Content-Type": "application/json"},
        body=load_fixture("radarr/queue.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_client.get_queue()
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:7878/api/v3/queue?page=1&pageSize=20&sortKey=timeleft&sortDirection=default&includeUnknownMovieItems=False",
        headers={"Content-Type": "application/json"},
        body=load_fixture("radarr/queue.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_client.get_queue(
        page=1,
        page_size=20,
        sort_key=RadarrSortKeys.TIMELEFT,
        sort_dir=PyarrSortDirection.DEFAULT,
        include_unknown_movie_items=False,
    )
    assert isinstance(data, dict)

    with contextlib.suppress(PyarrMissingArgument):
        data = radarr_client.get_queue(sort_key=RadarrSortKeys.TIMELEFT)
        assert False
    with contextlib.suppress(PyarrMissingArgument):
        data = radarr_client.get_queue(sort_dir=PyarrSortDirection.DEFAULT)
        assert False


@pytest.mark.usefixtures
def test_get_queue_details(responses, radarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:7878/api/v3/queue/details",
        headers={"Content-Type": "application/json"},
        body=load_fixture("radarr/queue_details.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_client.get_queue_details()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:7878/api/v3/queue/details?movieId=1&includeMovie=True",
        headers={"Content-Type": "application/json"},
        body=load_fixture("radarr/queue_details.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_client.get_queue_details(id_=1, include_movie=True)
    assert isinstance(data, list)


@pytest.mark.usefixtures
def test_get_queue_details(responses, radarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:7878/api/v3/queue/status",
        headers={"Content-Type": "application/json"},
        body=load_fixture("radarr/queue_status.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_client.get_queue_status()
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_del_queue_bulk(responses, radarr_client):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:7878/api/v3/queue/bulk",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/delete.json"),
        status=200,
    )
    data = radarr_client.del_queue_bulk(
        id_=[1, 2, 3], remove_from_client=True, blocklist=True
    )
    assert isinstance(data, dict)


# TODO: force_grab_queue_item


@pytest.mark.usefixtures
def test_get_indexer(responses, radarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:7878/api/v3/indexer",
        headers={"Content-Type": "application/json"},
        body=load_fixture("radarr/indexer_all.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_client.get_indexer()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:7878/api/v3/indexer/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("radarr/indexer.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_client.get_indexer(id_=1)
    assert isinstance(data, dict)
