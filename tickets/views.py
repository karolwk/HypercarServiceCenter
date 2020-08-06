from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from collections import deque

oil_queue = deque()
tires_queue = deque()
diagnostic_queue = deque()
tickets = {'change_oil': oil_queue, 'inflate_tires': tires_queue, 'diagnostic': diagnostic_queue}

def delete_from_tickets():
    if len(oil_queue) > 0:
        oil_queue.popleft()
    elif len(tires_queue) > 0:
        tires_queue.popleft()
    elif len(diagnostic_queue) > 0:
        diagnostic_queue.popleft()


def ticket_num():
    return len(oil_queue) + len(tires_queue) + len(diagnostic_queue)


def how_long(queue):

    if queue is oil_queue:
        return len(oil_queue) * 2
    if queue is tires_queue:
        return len(oil_queue) * 2 + len(tires_queue) * 5
    return len(oil_queue) * 2 + len(tires_queue) * 5 + len(diagnostic_queue) * 30


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class TicketMenu(View):
    menus = [{'change_oil': 'Change oil'},
             {'inflate_tires': 'Inflate tires'},
             {'diagnostic': 'Get diagnostic test'}]

    template_name = "tickets/menu.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'menus': self.menus, 'title': "Menu"})


class OilChange(View):
    def get(self, request, *args, **kwargs):
        long = how_long(oil_queue)
        oil_queue.append(ticket_num() + 1)
        return HttpResponse(f"<div>Your number is {ticket_num()}</div><div>Please wait around {long} minutes</div>")


class InflateTires(View):
    def get(self, request, *args, **kwargs):
        long = how_long(tires_queue)
        tires_queue.append(ticket_num() + 1)
        return HttpResponse(f"<div>Your number is {ticket_num()}</div><div>Please wait around {long} minutes</div>")


class Diagnostic(View):
    def get(self, request, *args, **kwargs):
        long = how_long(diagnostic_queue)
        diagnostic_queue.append(ticket_num() + 1)
        return HttpResponse(f"<div>Your number is {ticket_num()}</div><div>Please wait around {long} minutes</div>")


class Processing(View):
    template_name = "tickets/processing.html"

    def post(self, request, *args, **kwargs):
        delete_from_tickets()
        return render(request, self.template_name, {'tickets': tickets, 'title': 'Processing request'})


    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'tickets': tickets, 'title': 'Processing request'})


class Next(View):
    template_name = "tickets/next.html"


    def get(self, request, *args, **kwargs):
        queue = oil_queue + tires_queue + diagnostic_queue
        return render(request, self.template_name, {'queue': queue, 'title': 'Next client'})
