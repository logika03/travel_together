from datetime import datetime

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator

from django.views.generic import ListView, DetailView, TemplateView

from api.tasks import send_email_reset_password
from main.forms import SignUpForm, AuthForm, ImageForm, FindForm, ResetPasswordForm, ResetEmailForm
from main.models import Trip, TravelParticipant, FAQ, User, Transport
from main.services import get_trips, get_available_trips, change_trip_status


@method_decorator(login_required, name='dispatch')
class ApproveParticipant(TemplateView):
    def get(self, *args, **kwargs):
        return HttpResponse(status=404)

    def post(self, *args, **kwargs):
        trip_id = self.kwargs['trip_id']
        user_id = self.kwargs['user_id']
        trip = Trip.objects.filter(id=trip_id)
        if trip is None or trip.first().author != self.request.user:
            return HttpResponse(status=404)
        travel_participant = TravelParticipant.objects.filter(trip__id=trip_id, participant__id=user_id)
        if travel_participant is None:
            return HttpResponse(status=404)
        travel_participant = travel_participant.first()
        travel_participant.is_approved = True
        travel_participant.save()
        return redirect('account', pk=self.request.user.id)


class TripsPageListView(ListView):
    model = Trip
    template_name = 'main/trips.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TripsPageListView, self).get_context_data()
        change_trip_status()
        context['trips'] = get_available_trips()
        return context


class TripPageDetailView(DetailView):
    model = Trip
    template_name = 'main/trip.html'

    def get_context_data(self, **kwargs):
        context = super(TripPageDetailView, self).get_context_data()
        trip_pk = self.kwargs['pk']
        if self.request.user.is_authenticated:
            context['exists_participant'] = TravelParticipant.objects.filter(
                trip__id=trip_pk,
                participant=self.request.user) \
                .exists()
            trip = Trip.objects.get(id=trip_pk)
            context['is_own'] = trip.author_id == self.request.user.id
        context['participants'] = TravelParticipant.objects.filter(trip__id=trip_pk, is_approved=True)
        return context


class FindView(ListView):
    model = Trip
    template_name = 'main/find.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FindView, self).get_context_data()
        context['transports'] = Transport.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = FindForm(request.POST)
        trips = None
        message = ''
        if form.is_valid():
            country = form.cleaned_data['country']
            city = form.cleaned_data['city']
            transport = form.cleaned_data['transport']
            date = form.cleaned_data['date']
            trips = Trip.objects.filter(country=country, is_available=True)
            if city:
                trips = trips.filter(city=city)
            if date:
                trips = trips.filter(date=date)
            if transport:
                trips = trips.filter(transport__in=transport)
            if trips:
                message = 'Ничего не найдено. Проверьте правильность ввода.'
        else:
            for filed in form.errors:
                print(f'{filed}: {form.errors[filed].as_text()}')
        transports = Transport.objects.all()
        return render(request, self.template_name, {
            'trips': trips,
            'message': message,
            'transports': transports
        })


def main_page(request):
    trips = get_available_trips()
    response = render(request, 'main/main.html', {
        'trips': trips,
        'user': request.user,
    })
    return response


def login_view(request):
    if request.user.is_authenticated:
        return redirect('account', pk=request.user.id)
    form = None
    if request.method == 'POST':
        form = AuthForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is None:
                form.add_error('email', 'Неправильные email или пароль')
            else:
                login(request, user)
                return redirect('account', pk=user.id)
    else:
        form = AuthForm()
    return render(request, 'main/login.html', {
        'form': form,
    })


@method_decorator(login_required, name='dispatch')
class AccountView(DetailView):
    model = User
    template_name = 'main/account.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super(AccountView, self).get_context_data()
        pk = self.kwargs['pk']
        context['cur_trips'] = get_trips(pk, True)
        context['prev_trips'] = get_trips(pk, False)
        context['is_own'] = self.request.user.id == pk
        context['transports'] = Transport.objects.all()
        context['trips_participants'] = self.request.user.trips_participants.all()
        context['my_trips_participants'] = TravelParticipant.objects.filter(trip__author=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        request = self.request
        pk = self.kwargs['pk']
        if pk != request.user.id:
            return HttpResponse(status=404)
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            user = self.request.user
            user.avatar = request.FILES['avatar']
            user.save()
        else:
            for filed in form.errors:
                print(f'{filed}: {form.errors[filed].as_text()}')
        return redirect('account', pk=pk)


def logout_view(request):
    logout(request)
    return redirect('main')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('account', pk=request.user.id)
    form = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data['password1']
            user = form.save(commit=False)
            user.set_password(password1)
            user.save()
            login(request, user)
            return redirect('account', pk=request.user.id)
    else:
        form = SignUpForm()
    return render(request, 'main/signup.html', {
        'form': form,
    })


class FAQPageListView(ListView):
    model = FAQ
    template_name = 'main/faq.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FAQPageListView, self).get_context_data()
        context['faqs'] = FAQ.objects.values_list().order_by('-updated_at')
        return context


def test(request):
    return render(request, 'main/test.html')


def reset(request):
    if request.user.is_authenticated:
        return redirect('account', pk=request.user.id)
    form = None
    if request.method == 'POST':
        form = ResetEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            if user is None:
                form.add_error('email', 'Неправильные email')
                return render(request, 'main/reset.html', {
                    'form': form
                })
            send_email_reset_password(user.id, user.email, request)
            return redirect('sent_mail')

    return render(request, 'main/reset.html', {
        'form': form
    })


class ShowMessageSendMailView(TemplateView):
    template_name = 'main/show_message.html'

    def get_context_data(self, **kwargs):
        context = super(ShowMessageSendMailView, self).get_context_data()
        context['message'] = 'Следуйте инструкции в электронной почте'
        return context


class ShowMessageResetPasswordView(TemplateView):
    template_name = 'main/show_message.html'

    def get_context_data(self, **kwargs):
        context = super(ShowMessageResetPasswordView, self).get_context_data()
        context['message'] = 'Пароль успешно изменен'
        return context


def reset_password(request, pk):
    if request.user.is_authenticated:
        return redirect('account', pk=request.user.id)
    form = None
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = User.objects.get(id=pk)
            user.set_password(password)
            user.save()
            return redirect('changed_password')
        else:
            for filed in form.errors:
                print(f'{filed}: {form.errors[filed].as_text()}')
    return render(request, 'main/reset_password.html')


@method_decorator(login_required, name='dispatch')
class CreateTrip(TemplateView):
    def get(self):
        return HttpResponse(status=404)

    def post(self, request):
        form = FindForm(request.POST)

        if form.is_valid():
            country = form.cleaned_data['country']
            city = form.cleaned_data['city']
            date = form.cleaned_data['date']
            trip = Trip.objects.create(
                country=country,
                city=city,
                date=date,
                author=request.user,
            )
            transports = form.cleaned_data['transport']
            if len(transports) == 0:
                transports = Transport.objects.all()
            for transport in transports:
                trip.transport.add(transport)
            if trip.date >= datetime.now().date():
                trip.is_available = True
            trip.save()
            return redirect('account', pk=request.user.id)


@method_decorator(login_required, name='dispatch')
class AddParticipant(TemplateView):
    def get(self):
        return HttpResponse(status=404)

    def post(self, *args, **kwargs):
        trip_pk = self.kwargs['pk']
        trip = Trip.objects.filter(id=trip_pk).first()
        if trip is None:
            return HttpResponse(status=404)
        if len(TravelParticipant.objects.filter(trip__id=trip_pk, participant=self.request.user)) > 0 or \
                trip.author_id == self.request.user.id:
            message = 'Вы уже присоединились к поездке'
        else:
            TravelParticipant.objects.create(trip=trip, participant=self.request.user)
        return redirect('trip', pk=trip_pk)
