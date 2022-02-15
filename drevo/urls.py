from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import DrevoListView, DrevoView, ZnanieDetailView, \
    ZnanieByLabelView, AuthorDetailView, AuthorsListView, LabelsListView, GlossaryListView, ZnanieRatingView

urlpatterns = [
    path('category/<int:pk>', DrevoListView.as_view(), name='drevo_type'),
    path('', DrevoView.as_view(), name='drevo'),
    path('znanie/<int:pk>', ZnanieDetailView.as_view(), name='zdetail'),
    path('znanie/<int:pk>/vote/<str:vote>/', ZnanieRatingView.as_view(), name='znrating'),
    path('label/<int:pk>', ZnanieByLabelView.as_view(), name='zlabel'),
    path('author/<int:pk>', AuthorDetailView.as_view(), name='author'),
    path('authors/', AuthorsListView.as_view(), name='authors'),
    path('labels/', LabelsListView.as_view(), name='labels'),
    path('glossary/', GlossaryListView.as_view(), name='glossary'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
