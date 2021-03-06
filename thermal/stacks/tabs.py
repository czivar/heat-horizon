from django.utils.translation import ugettext_lazy as _

from horizon import messages
from horizon import exceptions
from horizon import tabs

from thermal import api

from .tables import ThermalEventsTable


class OverviewTab(tabs.Tab):
    name = _("Overview")
    slug = "overview"
    template_name = ("thermal/stacks/_detail_overview.html")

    def get_context_data(self, request):
        return {"stack": self.tab_group.kwargs['stack']}


class EventsTab(tabs.Tab):
    name = _("Events")
    slug = "events"
    template_name = "thermal/stacks/_detail_events.html"
    preload = False

    def get_context_data(self, request):
        stack = self.tab_group.kwargs['stack']
        try:
            events = api.heat.events_list(request, stack.stack_name)
        except Exception, e:
            events = []
            messages.error(request,
                           _('Unable to get events for stack "%s": %s') % \
                            (stack.stack_name, e))
            #exceptions.handle(request, ignore=True)
        return {"stack": stack,
                "table": ThermalEventsTable(request, data=events), }


class StackDetailTabs(tabs.TabGroup):
    slug = "stack_details"
    tabs = (OverviewTab, EventsTab)
    sticky = True
