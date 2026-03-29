from .models import Card, Plan, Response, Rejection, ProgressComment, DailyPlan, Exercise, Meal, Portfolio, User
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from .forms import CardForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.utils import timezone





def homepage(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('homepage')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def client_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'CLIENT':
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return _wrapped_view
def trainer_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'TRAINER':
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return _wrapped_view

@client_required
def myCards(request):
    cards = Card.objects.filter(client=request.user).order_by('-created_at')

    context = {
        'cards': cards
    }
    return render(request, 'client/my_cards.html', context)

@client_required
def createCard(request):
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.client = request.user
            card.status = 'AVAILABLE'
            card.save()
            messages.success(request, "Oglas uspješno kreiran!")
            return redirect('mycards')
    else:
        form = CardForm()
    context = {
        'form': form,
        'action': 'Kreiraj'
               }
    return render(request, 'client/card_form.html', context)

@client_required
def editCard(request, pk):
    card = get_object_or_404(Card, pk=pk, client=request.user)

    if 'save' in request.POST:
        form = CardForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            messages.success(request, "Oglas ažuriran!")
            return redirect('detailcard', pk=card.pk)
    elif 'delete' in request.POST:
        card.delete()
        messages.warning(request, "Oglas uspješno obrisan!")
        return redirect('mycards')
    else:
        form = CardForm(instance=card)

    context = {
        'form': form,
        'action': 'Uredi'
               }
    return render(request, 'client/card_form.html', context)

@client_required
def clientCardDetail(request, pk):
    card = get_object_or_404(Card, pk=pk, client=request.user)

    responses = card.response.all().order_by('-created_at')

    context = {
        'card': card,
        'responses': responses,
    }
    return render(request, 'client/detail.html', context)

def trainerCardDetail(request, pk):
    card = get_object_or_404(Card, pk=pk)
    already_responded = card.response.filter(trainer=request.user).exists()

    context = {
        'card': card,
        'already_responded': already_responded,
    }
    return render(request, 'trainer/detail.html', context)

def card_list(request):
    responded_card_ids = Response.objects.filter(
        trainer=request.user
    ).values_list('card_id', flat=True)
    
    cards = Card.objects.filter(
        status='AVAILABLE'
    ).exclude(
        id__in=responded_card_ids
    ).order_by('-created_at')
    
    context = {'cards': cards}
    return render(request, 'trainer/cards.html', context)

@login_required
def create_response(request, card_pk):
    card = get_object_or_404(Card, pk=card_pk, status='AVAILABLE')

    if request.user.role != 'TRAINER':
        return redirect('homepage')
    if card.response.filter(trainer=request.user).exists():
        return redirect('trainerCardDetail', pk=card_pk)

    if request.method == 'POST':
        pitch = request.POST.get('pitch')
        price_per_day = request.POST.get('price_per_day')
        duration_days = request.POST.get('duration_days')

        Response.objects.create(
            card=card,
            trainer=request.user,
            pitch=pitch,
            price_per_day=price_per_day,
            duration_days=duration_days,
            status='PENDING'
        )

        return redirect('card_list')

    context = {'card': card}
    return render(request, 'trainer/create_response.html', context)

@login_required
@client_required
def handleResponse(request, pk):
    response = get_object_or_404(Response, id=pk)
    card = response.card
    action = request.POST.get('action')
    if action == 'accept':
            response.status = 'ACCEPTED'
            card.status = 'CLOSED'
            response.save()
            card.save()

    elif action == 'decline':
        response.status = 'DECLINED'
        response.save()

    return redirect('clientCardDetail', pk=card.id)

@login_required
def allPlans(request):

    plansTrainer = Plan.objects.filter(trainer=request.user).order_by('-created_at')
    plansClient = Plan.objects.filter(client=request.user).order_by('-created_at')
    plans=[]
    if plansTrainer.exists():
        plans = plansTrainer
    elif plansClient.exists():
        plans = plansClient
    else:
        plans = Plan.objects.none()
    responses=[]
    responsesClient= Response.objects.filter(card__client=request.user).order_by('-created_at')
    responsesTrainer= Response.objects.filter(trainer=request.user).order_by('-created_at')
    if responsesClient.exists():
        responses=responsesClient
    elif responsesTrainer.exists():
        responses=responsesTrainer
    context = {
        'plans': plans,
        'responses': responses,
    }
    return render(request, 'plans/all_plans.html', context)

@login_required
def detailPlan(request, plan_pk):
    plan=get_object_or_404(Plan, pk=plan_pk)
    daily_plans = plan.dailyplan_set.all()
    if plan.client == request.user or plan.trainer == request.user:
        context = {
            'plan': plan,
            'daily_plans': daily_plans,
        }
        return render(request, 'plans/detail_plan.html', context)

@login_required
def createPlan(request, response_pk):
    response = get_object_or_404(Response, pk=response_pk)
    if request.method == 'POST':
        if response.trainer == request.user:
            if response.status == 'ACCEPTED' and not Plan.objects.filter(response=response).exists():
                duration = request.POST.get('duration')
                description = request.POST.get('description')
                plan = Plan.objects.create(
                    response=response,
                    client=response.card.client,
                    trainer=response.trainer,
                    description=description,
                    duration=duration,
                    isActive=True
                )
                messages.success(request, "Plan uspješno kreiran!")
                return redirect('detailplan', plan_pk=plan.pk)
            return redirect('allPlans')
        return redirect('allPlans')
    else:
        context = {
            'response': response,
        }
        return render(request, 'plans/create_plan.html', context)

@login_required
def cancelPlan(request,plan_pk):
    plan=get_object_or_404(Plan, pk=plan_pk)
    if request.user == plan.client or request.user == plan.trainer:

        if request.method == 'POST' and plan.isActive==True:
            reason= request.POST.get('reason')
            Rejection.objects.create(plan=plan, author=request.user, reason=reason)
            plan.isActive=False
            plan.save()
            messages.warning(request, "Plan uspješno prekinut!")
            return redirect('detailplan', plan_pk=plan.pk)
        else:
            context = {
                'plan': plan,
            }
            return render(request, 'plans/cancel_plan.html', context)
    return redirect('detailplan', plan_pk=plan.pk)

@login_required
def showComments(request, plan_pk):
    plan = get_object_or_404(Plan, pk=plan_pk)
    if plan.client == request.user or plan.trainer == request.user:

        comments = plan.progresscomment_set.all().order_by('-created_at')
        context = {
            'plan': plan,
            'comments': comments,
        }
        return render(request, 'plans/show_comments.html', context)

@login_required
def addComment(request, plan_pk):
    plan=get_object_or_404(Plan, pk=plan_pk)
    if plan.client == request.user or plan.trainer == request.user:

        if request.method == 'POST' :
            comment= request.POST.get('comment')
            ProgressComment.objects.create(author=request.user, plan=plan, comment=comment)
            messages.success(request, "Komentar uspješno dodan!")
            return redirect('detailplan', plan_pk=plan.pk)
    return redirect('detailplan', plan_pk=plan.pk)


@trainer_required
def addDailyPlan(request, plan_pk):
    plan=get_object_or_404(Plan, pk=plan_pk)
    if plan.trainer == request.user :
        if request.method == 'POST' and plan.isActive==True:
            if plan.dailyplan_set.count()<7:
                description = request.POST.get('description')
                DailyPlan.objects.create(plan=plan, description=description)
                messages.success(request, "Dnevni plan uspješno dodan!")
                
            return redirect('detailplan', plan_pk=plan.pk)
        else:
            context = {
                'plan': plan,
            }
            return render(request, 'plans/add_daily_plan.html', context)

@trainer_required
def addExercise(request, dailyplan_pk):
    daily_plan = get_object_or_404(DailyPlan, pk=dailyplan_pk)
    if daily_plan.plan.trainer == request.user:
        if request.method == 'POST' and daily_plan.plan.isActive==True:
            name = request.POST.get('name')
            description = request.POST.get('description')
            video_url = request.POST.get('video_url')
            sets = request.POST.get('sets')
            reps = request.POST.get('reps')
            Exercise.objects.create(
                dailyPlan=daily_plan,
                name=name,
                description=description,
                video_url=video_url,
                sets=sets,
                reps=reps
            )
            messages.success(request, "Vježba uspješno dodana!")
            return redirect('detailplan', plan_pk=daily_plan.plan.pk)
        else:
            context = {
                'daily_plan': daily_plan,
            }
            return render(request, 'plans/add_exercise.html', context)

@trainer_required
def addMeal(request, dailyplan_pk):
    daily_plan = get_object_or_404(DailyPlan, pk=dailyplan_pk)
    if daily_plan.plan.trainer == request.user:
        if request.method == 'POST' and daily_plan.plan.isActive==True:
            mealType = request.POST.get('mealType')
            name = request.POST.get('name')
            description = request.POST.get('description')
            image_url = request.POST.get('image_url')
            calories = request.POST.get('calories')
            Meal.objects.create(
                dailyPlan=daily_plan,
                mealType=mealType,
                name=name,
                description=description,
                image_url=image_url,
                calories=calories
            )
            messages.success(request, "Obrok uspješno dodan!")
            return redirect('detailplan', plan_pk=daily_plan.plan.pk)
        else:
            context = {
                'daily_plan': daily_plan,
            }
            return render(request, 'plans/add_meal.html', context)

@trainer_required
def editDailyPlan(request, dailyplan_pk):
    daily_plan = get_object_or_404(DailyPlan, pk=dailyplan_pk)
    if daily_plan.plan.trainer == request.user:
        if request.method == 'POST' and daily_plan.plan.isActive==True:
            description = request.POST.get('description')
            daily_plan.description = description
            daily_plan.save()
            messages.success(request, "Dnevni plan uspješno ažuriran!")
            return redirect('detailplan', plan_pk=daily_plan.plan.pk)
        else:
            context = {
                'daily_plan': daily_plan,
            }
            return render(request, 'plans/edit_daily_plan.html', context)

@trainer_required
def deleteExercise(request, exercise_pk):
    exercise = get_object_or_404(Exercise, pk=exercise_pk)
    if exercise.dailyPlan.plan.trainer == request.user and exercise.dailyPlan.plan.isActive==True:
        plan_pk = exercise.dailyPlan.plan.pk
        exercise.delete()
        messages.warning(request, "Vježba uspješno obrisana!")
        return redirect('detailplan', plan_pk=plan_pk)

@trainer_required
def deleteMeal(request, meal_pk):
    meal = get_object_or_404(Meal, pk=meal_pk)
    if meal.dailyPlan.plan.trainer == request.user and meal.dailyPlan.plan.isActive:
        plan_pk = meal.dailyPlan.plan.pk
        meal.delete()
        messages.warning(request, "Obrok uspješno obrisan!")
        return redirect('detailplan', plan_pk=plan_pk)
    
@login_required
def portfolio(request, trainer_id):
    trainer = get_object_or_404(User, id=trainer_id)
    portfolio = Portfolio.objects.filter(trainer=trainer).first()

    numberOfClients = Plan.objects.filter(trainer=trainer).count()
    offers = Response.objects.filter(trainer=trainer)
    totalOffers = offers.count()
    if totalOffers > 0:
        rejectedOffers = round(Response.objects.filter(trainer=trainer, status='DECLINED').count() / totalOffers * 100)
        acceptedOffers = round(Response.objects.filter(trainer=trainer, status='ACCEPTED').count() / totalOffers * 100)
        pendingOffers = 100 - rejectedOffers - acceptedOffers
    else:
        rejectedOffers = 0
        acceptedOffers = 0
        pendingOffers = 0
    avgPrice = offers.aggregate(Avg('price_per_day'))
    timeActive = (timezone.now().date() - trainer.date_joined.date()).days
    planExample = Plan.objects.filter(trainer=trainer, isActive=False).first()

    context = {'portfolio': portfolio,
               'trainer': trainer,
               'numberOfClients': numberOfClients,
               'totalOffers': totalOffers,
               'rejectedOffers': rejectedOffers,
               'acceptedOffers': acceptedOffers,
               'pendingOffers': pendingOffers,
               'avgPrice': avgPrice,
               'timeActive': timeActive,
               'planExample': planExample}
    return render(request, 'trainer/portfolio.html', context)

@trainer_required
def editPortfolio(request, trainer_id):
    trainer = get_object_or_404(User, id=trainer_id)
    if request.user != trainer:
        return redirect('homepage')

    portfolio = Portfolio.objects.filter(trainer=trainer).first()

    if request.method == 'GET':
        return render(request, 'trainer/portfolio/edit.html', {'trainer': trainer, 'portfolio': portfolio})

    if portfolio is None:
        Portfolio.objects.create(
            trainer=trainer,
            profession=request.POST.get('profession'),
            bio=request.POST.get('bio'),
            experience=request.POST.get('experience'),
            education=request.POST.get('education'),
            profile_image_url=request.POST.get('profile_image_url')
        )
    else:
        portfolio.profession = request.POST.get('profession')
        portfolio.bio = request.POST.get('bio')
        portfolio.experience = request.POST.get('experience')
        portfolio.education = request.POST.get('education')
        portfolio.profile_image_url=request.POST.get('profile_image_url')
        portfolio.save()

    return redirect('portfolio', trainer_id=trainer.id)
    
