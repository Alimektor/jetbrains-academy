from django.views import View
from django.views.generic.base import TemplateView
from django.http.response import HttpResponse
from django.shortcuts import redirect
from collections import deque


class ElectronicQueue:
    queue = {
        "change_oil": deque(),
        "inflate_tires": deque(),
        "diagnostic": deque()
    }
    next_ticket = None
    current_ticket = 1


class WelcomeView(View):
    def get(self):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuView(TemplateView):
    template_name = "templates/hypercar/index.html"
    links = {
        "change_oil": "Change oil",
        "inflate_tires": "Inflate tires",
        "diagnostic": "Get diagnostic test"
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["links"] = self.links.items()
        return context


class TicketView(TemplateView):
    template_name = "templates/hypercar/tickets.html"
    minutes_per_operation = {
        "change_oil": 2,
        "inflate_tires": 5,
        "diagnostic": 30
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        number = ElectronicQueue.current_ticket
        ElectronicQueue.current_ticket += 1
        ticket_type = kwargs["link"]
        minutes = 0
        for key, value in ElectronicQueue.queue.items():
            minutes += len(value) * self.minutes_per_operation[key]
            if key == ticket_type:
                break
        ElectronicQueue.queue[ticket_type].append(number)
        context["ticket_number"] = number
        context["minutes_to_wait"] = minutes
        return context


class ProcessView(TemplateView):
    template_name = "templates/hypercar/process.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["oil"] = len(ElectronicQueue.queue["change_oil"])
        context["tires"] = len(ElectronicQueue.queue["inflate_tires"])
        context["diagnostic"] = len(ElectronicQueue.queue["diagnostic"])
        return context

    def post(self, request, *args, **kwargs):
        if len(ElectronicQueue.queue["change_oil"]) > 0:
            ElectronicQueue.next_ticket = ElectronicQueue.queue["change_oil"].popleft()
        elif len(ElectronicQueue.queue["inflate_tires"]) > 0:
            ElectronicQueue.next_ticket = ElectronicQueue.queue["inflate_tires"].popleft()
        elif len(ElectronicQueue.queue["diagnostic"]) > 0:
            ElectronicQueue.next_ticket = ElectronicQueue.queue["diagnostic"].popleft()
        else:
            ElectronicQueue.next_ticket = None
        return redirect("/processing")


class NextView(TemplateView):
    template_name = "templates/hypercar/next.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if ElectronicQueue.next_ticket is not None:
            context["next_ticket_number"] = ElectronicQueue.next_ticket
        return context
