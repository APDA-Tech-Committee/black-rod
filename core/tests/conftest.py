import pytest
import django
from django.conf import settings
from django.test.utils import get_runner
from unittest.mock import MagicMock
import sys

# Mock dal.autocomplete to avoid import errors
class MockAutoComplete:
    class ModelSelect2:
        def __init__(self, *args, **kwargs):
            pass
    
    class ModelSelect2Multiple:
        def __init__(self, *args, **kwargs):
            pass

    class TaggitSelect2:
        def __init__(self, *args, **kwargs):
            pass

    class Select2QuerySetView:
        @classmethod 
        def as_view(cls):
            def view(request, *args, **kwargs):
                from django.http import JsonResponse
                return JsonResponse({'results': []})
            return view

# Mock the dal modules first
dal_mock = MagicMock()
dal_mock.autocomplete = MockAutoComplete()
sys.modules['dal'] = dal_mock
sys.modules['dal.autocomplete'] = MockAutoComplete()

# Also mock the school views that use dal
from unittest.mock import Mock

# Create mock views modules
school_views_mock = Mock()
video_views_mock = Mock()
debater_views_mock = Mock()
team_views_mock = Mock() 
tournament_views_mock = Mock()

# Create a mock class with as_view method
class MockViewClass:
    @classmethod
    def as_view(cls, **kwargs):
        def view(request, *args, **view_kwargs):
            from django.http import JsonResponse
            return JsonResponse({'results': []})
        return view

# Apply the mock to all the views
for mock_module in [school_views_mock, video_views_mock, debater_views_mock, team_views_mock, tournament_views_mock]:
    for attr_name in [
        'SchoolAutocomplete', 'DebaterAutocomplete', 'TeamAutocomplete', 'TagAutocomplete',
        'TournamentAutocomplete', 'AllTournamentAutocomplete',
        'SchoolListView', 'SchoolDetailView', 'SchoolUpdateView', 'SchoolDeleteView', 'SchoolCreateView',
        'DebaterListView', 'DebaterDetailView', 'DebaterUpdateView', 'DebaterDeleteView', 'DebaterCreateView',
        'TeamListView', 'TeamDetailView', 'TeamUpdateView', 'TeamDeleteView',
        'VideoListView', 'VideoDetailView', 'VideoUpdateView', 'VideoDeleteView', 'VideoCreateView', 'TagDetail',
        'TournamentListView', 'TournamentDetailView', 'TournamentUpdateView', 'TournamentDeleteView', 'TournamentCreateView',
        'ScheduleView', 'TournamentDataEntryWizardView', 'TournamentImportWizardView'
    ]:
        setattr(mock_module, attr_name, MockViewClass)

sys.modules['core.views.school_views'] = school_views_mock
sys.modules['core.views.video_views'] = video_views_mock
sys.modules['core.views.debater_views'] = debater_views_mock
sys.modules['core.views.team_views'] = team_views_mock
sys.modules['core.views.tournament_views'] = tournament_views_mock


def pytest_configure():
    """Configure Django for pytest"""
    settings.configure(
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
            }
        },
        SITE_ID=1,
        SECRET_KEY='test-secret-key-for-pytest-only',
        USE_I18N=True,
        USE_L10N=True,
        STATIC_URL='/static/',
        ROOT_URLCONF='core.tests.urls',  # Use a test-specific URL config
        TEMPLATE_LOADERS=(
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ),
        MIDDLEWARE=[
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ],
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'django.contrib.admin',
            'taggit',  # Add taggit for migrations compatibility
            'allauth',
            'allauth.account',
            'django_summernote',  # Add for URL includes
            'core.apps.CoreConfig',  # Use the proper app config
            'apdaonline',
        ],
        PASSWORD_HASHERS=(
            'django.contrib.auth.hashers.MD5PasswordHasher',
        ),
        # Add authentication backends for allauth
        AUTHENTICATION_BACKENDS=[
            'django.contrib.auth.backends.ModelBackend',
            'allauth.account.auth_backends.AuthenticationBackend',
        ],
        # Add SEASONS setting needed by forms
        SEASONS=tuple(
            (str(year), f"{year}-{str(year+1)[2:]}")
            for year in range(2025, 2003, -1)  # LATEST to OLDEST-1
        ),
        CURRENT_SEASON='2024',
        ENV='test',  # Add ENV setting for migrations
        # Add HAYSTACK_CONNECTIONS for search functionality
        HAYSTACK_CONNECTIONS = {
            'default': {
                'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
            },
        },
        # Disable migrations for faster testing
        MIGRATION_MODULES={
            'core': None,
            'auth': None,
            'contenttypes': None,
            'sessions': None,
            'taggit': None,
        },
    )
    
    django.setup()


# Clean up - remove custom fixtures that cause scope issues
# pytest-django will handle database setup automatically
