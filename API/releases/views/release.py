from rest_framework.response import Response
from rest_framework.views import APIView

from API.releases.models.release import Release
from API.releases.serializer.release import ReleaseSerializer


class LoadReleases(APIView):
    permission_classes = ()

    @staticmethod
    def get(request):
        """
        Load releases, can be filtered by type
        """
        start_date = request.query_params.get('date')
        direction = request.query_params.get('direction', None)
        release_type = 'event' if request.query_params.get('type') == 'release' else 'release'
        if direction == "1":
            dates = Release.objects.filter(release_date__gt=start_date).order_by(
                "release_date").values('release_date')[:5]
            releases = Release.objects.filter(release_date__in=dates)
        elif direction == "0":
            dates = Release.objects.filter(release_date__lt=start_date).order_by(
                "-release_date").values('release_date')[:5]
            releases = Release.objects.filter(release_date__in=dates)
        else:
            dates_past = Release.objects.filter(release_date__lt=start_date).order_by(
                "-release_date").values('release_date')[:5]

            dates_future = Release.objects.filter(release_date__gt=start_date).order_by(
                "release_date").values('release_date')[:5]

            releases_future = Release.objects.filter(release_date__in=dates_past).order_by(
                "release_date")
            releases_past = Release.objects.filter(release_date__in=dates_future).order_by(
                "-release_date")
            releases_today = Release.objects.filter(release_date=start_date)
            releases = releases_future | releases_past | releases_today

        serialized_releases = ReleaseSerializer(
            releases,
            many=True
        ).data

        total = len(releases)

        first = Release.objects.filter(release_type=release_type).order_by('id')[0].release_date
        last = Release.objects.filter(release_type=release_type).order_by('-id')[0].release_date

        return Response({"releases": serialized_releases,
                         "releases_start": first,
                         "releases_end": last,
                         "total": total})
