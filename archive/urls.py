from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^event/(?P<event_id>[0-9]+)/$', views.event, name='event'),
    url(r'^runner/(?P<runner_id>[0-9]+)/$', views.runner, name='runner'),
    url(r'^series/(?P<series_id>[0-9]+)/$', views.series, name='series'),
    url(r'missing_data/$', views.missing_data, name='missing_data'),
    url(r'^series/$', views.series_list, name='series_list'),
    url(r'^events/$', views.events_list, name='events_list'),
    url(r'^runners/$', views.runners_list, name='runners_list'),
    url(r'^tools/$', views.tools, name='tools'),
    url(r'^tools/reimport/$', views.reimport, name='reimport'),
    url(r'^tools/merge_runners/$', views.merge_duplicate_runners, name='merge_runners'),
    url(r'^tools/move_course/$', views.move_course, name='move_course'),
    url(r'^tools/remove_ghost_results/$', views.remove_ghost_results, name='remove_ghost_results'),
    url(r'^series/(?P<series_id>[0-9]+)/overall_results/$', views.overall_results, name='overall_results'),
    url(r'^events/map/$', views.events_on_map, name='events_on_map'),

]