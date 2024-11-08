from django.shortcuts import render,redirect
from .models import*

from django.db.models import Sum,F
from decimal import Decimal
from .forms import RegistrationForm,ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth import authenticate, login,logout
from django.utils import timezone


from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import io
from io import BytesIO
import base64
import requests
import pandas as pd

import json
# Create your views here.
# n3P1BNiUUGUMiYKsI+AOnw==MjowgehwIMMHfgRM



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user)
            

            return redirect('/loginn/')  
    else:
        form = RegistrationForm()
        print(form)
    context={'form':form}
    return render(request,'register.html',context)
def register_view(request):
    form=RegistrationForm()
    print(form)
    context={'form':form}

    return render(request,'register.html',context)
def index(request):
   
    return render(request,'login.html')


def loginn(request):
    
    if request.method=="POST":
        
        username=request.POST.get('name')
        password=request.POST.get('pswd')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/home')  # Redirect to your home page on successful login
        else:
            error_message = "Invalid login credentials"  # You can customize the error message
            return render(request, 'login.html', {'messages': error_message})
    

    return render(request,'login.html')


def user_logout(requset):
    logout(requset)
    return redirect('/')


@login_required(login_url='/loginn/')
def profile(request):
    
    return render(request,'profile.html',{'user': request.user})

@login_required(login_url='/loginn/')
def editprofile(request):
    user = request.user

    if request.method == 'POST':
        # username=request.POST['user']
        email=request.POST['email']
        # gender=request.POST['gender']
        weight=request.POST['weight']
        age=request.POST['age']
        height=request.POST['height']
        # user.username=username
        
        user.email = email
        # user.gender = gender
        user.weight = weight
        user.height = height
        user.age = age

        user.save() 
        
        return redirect('profile')  # Redirect to the user's profile page after successful update
    else:
        context = {'user':user}
        return render(request, 'editprofile.html', context)

@login_required(login_url='/loginn/')
def home(request):
    
    user=request.user
    weight=float(user.weight)
    height=float(user.height)
    gender=user.gender
    age=user.age
    today = timezone.now().date()
# Male-BMR = 10 * weight (kg) + 6.25 * height (cm) - 5 * age (years) + 5
# Female-BMR = 10 * weight (kg) + 6.25 * height (cm) - 5 * age (years) - 161
    if gender=="M":
        BMR=(weight*10)+(6.25*height)-(5*age)+5
    else:
        BMR=(weight*10)+(6.25*height)-(5*age)-161
    BMR = float(BMR)

    sedentary=round(1.2*BMR,2)
    lightly_active=round(1.4*BMR,2)
    moderately_active=round(1.55*BMR,2)
    very_active=round(1.73*BMR,2)
    extremely_active=round(1.9*BMR,2)

    food_logs_today = FoodLog.objects.filter(user=request.user, created_at=today)
    consumed_today = food_logs_today.aggregate(Sum('calories'))['calories__sum'] or 0
    consumed_today = float(consumed_today)
    remaining_calories = round(BMR - consumed_today,2)
    # if consumed_today>remaining_calories:
    #     consumed_today=remaining_calories
    #     msg=""
    remaining_calories = max(0, remaining_calories)
    consumed_today = max(0, consumed_today)

    labels = ['Remaining Calories', 'Calories Consumed']
    data = [remaining_calories, consumed_today]
    # colors = ['#36A2EB', '#FF6384']

    # Create a doughnut chart
    fig, ax = plt.subplots(figsize=(6, 6))
    wedges, texts, autotexts = ax.pie(data, autopct='%1.1f%%', startangle=90, wedgeprops=dict(width=0.4))
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

    # Add a circle in the center to create a doughnut chart
    center_circle = plt.Circle((0, 0), 0.70, fc='#12151e')
    fig = plt.gcf()
    fig.gca().add_artist(center_circle)
    fig.patch.set_facecolor('#12151e')
    for text, autotext, label in zip(texts, autotexts, labels):

        autotext.set_text(f'{label}\n{data[labels.index(label)]}') 
        autotext.set_color('white')  # Clear default text
        autotext.set_fontsize(20)
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=58, bbox_inches='tight')
    plt.close(fig)
    buffer.seek(0)
    chart_data = base64.b64encode(buffer.read()).decode('utf-8')    
    context={'BMR':BMR,
            'sedentary':sedentary,
            'lightly_active':lightly_active,
            'moderately_active':moderately_active,
            'very_active':very_active,
            'extremely_active':extremely_active,
            'remaining_calories': remaining_calories,
            'consumed_today': consumed_today,
            'chart_data': chart_data
    }
    return render(request, 'home.html',context)


@login_required(login_url='/loginn/')
def dayLog(request):
    today = timezone.now().date()
    # print(today)
    breakfast = FoodLog.objects.filter(user=request.user, created_at=today,category="breakfast")
    # print(breakfast)
    breakfast_total= breakfast.aggregate(Sum('calories'))['calories__sum'] or 0
    breakfast_total = round(float(breakfast_total),2)
    

    lunch = FoodLog.objects.filter(user=request.user, created_at=today,category="lunch")
    lunch_total= lunch.aggregate(Sum('calories'))['calories__sum'] or 0
    lunch_total = round(float(lunch_total),2)

    dinner = FoodLog.objects.filter(user=request.user, created_at=today,category="dinner")
    dinner_total= dinner.aggregate(Sum('calories'))['calories__sum'] or 0
    dinner_total = round(float(dinner_total),2)

    snack = FoodLog.objects.filter(user=request.user, created_at=today,category="snack")
    snack_total= snack.aggregate(Sum('calories'))['calories__sum'] or 0
    snack_total = round(float(snack_total),2)

    exercise=ExerciseLog.objects.all().filter(user=request.user,created_at=today)
    
    e_total= exercise.aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0
    e_total=round(float(e_total),2)

    
    context={
        'breakfast_total':breakfast_total,
        'lunch_total':lunch_total,
        'dinner_total':dinner_total,
        'snack_total':snack_total,
        'e_total':e_total
    }
    return render(request, 'daily_log.html', context)
# @login_required(login_url='/loginn/')

# def setCategory(request):
#     ii=request.GET.get('category')
#     print(ii)
#     FoodLog.objects.create(user=request.user,category=ii)
#     return redirect('/add_meal/')

@login_required(login_url='/loginn/')
def add_meal(request):
    ii=request.GET.get('category')
    
    if request.method=='POST':
        query=request.POST.get('query')

        
        
        url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
           
        headers={'Content-Type': 'application/json','x-app-id': '9bcc65ef','x-app-key': 'a72c336556ff8e212aa79f7ddce270dd'}
        food_items = query.split(' and ')
        print(food_items)
        all_food_data=[]

        for food_item in food_items:
            data = {"query": food_item}

            try:
                response = requests.post(url, headers=headers, json=data)
                response.raise_for_status()  
                nutrient_data = response.json()
                food_name = nutrient_data.get('foods')[0].get('food_name') if nutrient_data.get('foods') else ''
                calories = nutrient_data.get('foods')[0].get('nf_calories') if nutrient_data.get('foods') else ''
                serving_unit = nutrient_data.get('foods')[0].get('serving_unit') if nutrient_data.get('foods') else ''
                weight = nutrient_data.get('foods')[0].get('serving_weight_grams') if nutrient_data.get('foods') else ''
                quantity = nutrient_data.get('foods')[0].get('serving_qty') if nutrient_data.get('foods') else ''
                all_food_data.append({
                                    'food_name': food_name,
                                    'calories': round(calories,2),
                                    'quantity': round(quantity,2),
                                    'serving_unit': serving_unit,
                                    'weight': weight
                                })
                FoodLog.objects.create(user=request.user,food_consumed=food_name,calories=calories,quantity=quantity,unit=serving_unit,serving_weight=weight,category=ii)
            except requests.exceptions.RequestException as e:
                messages.error(request, str(e))
                return redirect('/dayLog/')            
    return redirect('/dayLog/')
@login_required(login_url='/loginn/')
          
def add_exercise(request):
    if request.method=='POST':
        query=request.POST.get('query')

        
        
        url = 'https://trackapi.nutritionix.com/v2/natural/exercise'
           
        headers={'Content-Type': 'application/json','x-app-id': '9bcc65ef','x-app-key': 'a72c336556ff8e212aa79f7ddce270dd'}
        # api_request= requests.get(api_url,})
        # print(api_request.content)
        exercises = query.split(' and ')
        all_exercise=[]

        for exercise in exercises:
            data = {"query": exercise}

            try:
                response = requests.post(url, headers=headers, json=data)
                response.raise_for_status()  # Raise an exception for bad responses (4xx and 5xx)
                exercise_data = response.json()
                print(exercise_data)
                if not exercise_data['exercises']:
                    messages.error(request, 'Not Found!!!!')
                    return redirect('/dayLog/')
                exercise_name = exercise_data.get('exercises')[0].get('name') if exercise_data.get('exercises') else ''
                calories = exercise_data.get('exercises')[0].get('nf_calories') if exercise_data.get('exercises') else ''
                duration_mn = exercise_data.get('exercises')[0].get('duration_min') if exercise_data.get('exercises') else ''
                all_exercise.append({
                                    'exercise_name': exercise_name,
                                    'calories': calories,
                                    'duration': duration_mn
                                })
                print(all_exercise)
                ExerciseLog.objects.create(user=request.user,exercise_name=exercise_name,calories_burned=calories,duration_minutes=duration_mn,description=query)
            except requests.exceptions.RequestException as e:
                messages.error(request, str(e))
                return redirect('/dayLog/') 
            return redirect('/dayLog/')




@login_required(login_url='/loginn/')
def view_logs(request):
    if request.method=='POST':
        date=request.POST['date']
        if date:
            flogs=FoodLog.objects.all().filter(user=request.user,created_at=date)
            elogs=ExerciseLog.objects.all().filter(user=request.user,created_at=date)
            return render(request,'view_logs.html',{'flogs':flogs,'elogs':elogs})

    flogs=FoodLog.objects.all().filter(user=request.user,created_at=timezone.now().date())
    elogs=ExerciseLog.objects.all().filter(user=request.user,created_at=timezone.now().date())

    return render(request,'view_logs.html',{'flogs':flogs,'elogs':elogs})

@login_required(login_url='/loginn/')
def deletefood(request):
    id=request.GET.get('id')
    var=FoodLog.objects.get(id=id)
    date=var.created_at
    var.delete()
    flogs=FoodLog.objects.all().filter(user=request.user,created_at=date)
    elogs=ExerciseLog.objects.all().filter(user=request.user,created_at=date)

    return render(request,'view_logs.html',{'flogs':flogs,'elogs':elogs})


@login_required(login_url='/loginn/')
    
def deleteexercise(request):
    id=request.GET.get('id')
    var=ExerciseLog.objects.get(id=id)
    date=var.created_at
    var.delete()
    flogs=FoodLog.objects.all().filter(user=request.user,created_at=date)
    elogs=ExerciseLog.objects.all().filter(user=request.user,created_at=date)

    return render(request,'view_logs.html',{'flogs':flogs,'elogs':elogs})
@login_required(login_url='/loginn/')
 
def deleteweight(request):
    id=request.GET.get('id')
    var=Weight.objects.filter(id=id)
    var.delete()
    return HttpResponseRedirect('/goal/')


@login_required(login_url='/loginn/')
 
def editfood(request):
    id=request.GET.get('id')
    var=FoodLog.objects.get(id=id)
    date=var.created_at
    if request.method=='POST':
        category=request.POST.get('category')
        food=request.POST['food']
        print(category,food)
        qty=request.POST.get('qty')
        print(qty)
        category=category.lower()
        if category not in ['breakfast', 'lunch', 'dinner','snacks','snack']:
            messages.error(request, 'Wrong category')
            return render(request, 'edit_flog.html', {'var': var})
        if food is not None and qty is not None:
            query=food+' '+qty

        print(query)
        
        url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
           
        headers={'Content-Type': 'application/json','x-app-id': '9bcc65ef','x-app-key': 'a72c336556ff8e212aa79f7ddce270dd'}
        # food_items = query.split(' and ')
        # all_food_data=[]

        # for food_item in food_items:
        data = {"query": query}

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()  
            nutrient_data = response.json()
            food_name = nutrient_data.get('foods')[0].get('food_name') if nutrient_data.get('foods') else ''
            calories = nutrient_data.get('foods')[0].get('nf_calories') if nutrient_data.get('foods') else ''
            serving_unit = nutrient_data.get('foods')[0].get('serving_unit') if nutrient_data.get('foods') else ''
            weight = nutrient_data.get('foods')[0].get('serving_weight_grams') if nutrient_data.get('foods') else ''
            quantity = nutrient_data.get('foods')[0].get('serving_qty') if nutrient_data.get('foods') else ''
            
            FoodLog.objects.filter(id=id).update(user=request.user,food_consumed=food_name,calories=calories,quantity=quantity,unit=serving_unit,serving_weight=weight,category=category)
        except requests.exceptions.RequestException as e:
            messages.error(request, str(e))
            return render(request,'edit_flog.html',{'var':var}) 
        flogs=FoodLog.objects.all().filter(user=request.user,created_at=date)
        elogs=ExerciseLog.objects.all().filter(user=request.user,created_at=date)

        return render(request,'view_logs.html',{'flogs':flogs,'elogs':elogs})

    else:
        return render(request,'edit_flog.html',{'var':var})


    
@login_required(login_url='/loginn/')
    
def editexercise(request):
    id=request.GET.get('id')
    var=ExerciseLog.objects.filter(id=id)
    date=var.dates
    if request.method=='POST':
        name=request.POST['name']
        time=request.POST['time']
        if name is not None and time is not None:
            query=name+' '+time+' '+'minutes'
        
        
        url = 'https://trackapi.nutritionix.com/v2/natural/exercise'
           
        headers={'Content-Type': 'application/json','x-app-id': '9bcc65ef','x-app-key': 'a72c336556ff8e212aa79f7ddce270dd'}
        # api_request= requests.get(api_url,})
        # print(api_request.content)
        

      
        data = {"query": query}
        print(data)
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()  # Raise an exception for bad responses (4xx and 5xx)
            exercise_data = response.json()
            print(exercise_data)
            if not exercise_data['exercises']:
                    messages.error(request, 'Not Found!!!!')
                    return redirect('/view_logs/')
            exercise_name = exercise_data.get('exercises')[0].get('name') if exercise_data.get('exercises') else ''
            if exercise_name != name and exercise_name== "walking":
                messages.error(request, 'Not Found!!!!')
                return redirect('/view_logs/')
            calories = exercise_data.get('exercises')[0].get('nf_calories') if exercise_data.get('exercises') else ''
            duration_mn = exercise_data.get('exercises')[0].get('duration_min') if exercise_data.get('exercises') else ''
            
            ExerciseLog.objects.filter(id=id).update(user=request.user,exercise_name=exercise_name,calories_burned=calories,duration_minutes=duration_mn)
        except requests.exceptions.RequestException as e:
            messages.error(request, str(e))
            return redirect('/view_logs/') 
        return redirect('/view_logs/')
    return  render(request,'edit_elog.html',{'var':var})
def editweight(request):
    id=request.GET.get('id')
    var=Weight.objects.filter(id=id)
    if request.method=='POST':
        weight=request.POST['weight']
        date=request.POST['date']
        var.update(weight=weight,date=date)
        # var.date=date
        return redirect('/goal/')

    
    return render(request,'editweight.html',{'var':var})
        


@login_required(login_url='/loginn/')
 
def food(request):
    query = 'egg and bread and peanuts and mushrooms and Apple and Banana and Chicken and beef and spinach and broccoli and oatmeal and greek yogurt and carrots and tomatoes and rice'
    
    api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
    response = requests.get(api_url, headers={'X-Api-Key': 'n3P1BNiUUGUMiYKsI+AOnw==MjowgehwIMMHfgRM'})
    
    if response.status_code == requests.codes.ok:
        data=response.json()
        
    else:
        print("Error:", response.status_code, response.text)
    
    if data:
        
        i=0
        for food_data in data:
            i=i+1
            # Extract relevant information
            
            food_name = food_data['name']
            serving_size = food_data['serving_size_g']
            calories = food_data['calories']
            fat = food_data['fat_total_g']
            protein=food_data['protein_g']
            carbohydrates = food_data['carbohydrates_total_g']
            fiber=food_data['fiber_g']
            sugar=food_data['sugar_g']
            print(fiber,sugar)
            cholestrol=food_data['cholesterol_mg']
            Food.objects.create(food_name=food_name,calories=calories,serving_size=serving_size,fat=fat,protein=protein,
                                carbohydrates=carbohydrates,fiber=fiber,sugar=sugar,cholestrol=cholestrol)

                
    return render(request,'home.html')

@login_required(login_url='/loginn/')

def goal(request):
    if request.method=="POST":
        weight=request.POST['weight']
        date=request.POST['date']
        var=Weight.objects.create(user=request.user,weight=weight,date=date)
        var.save()

    
    queryset = Weight.objects.all().filter(user=request.user).order_by('date')
    
    
    weight_data = [{'date_logged': item.date, 'weight': item.weight} for item in queryset]

    context = {'weight_data': weight_data,'queryset':queryset}
    return render(request,'goal.html',context)
   

@login_required(login_url='/loginn/')
 
def food_list_view(request):
    
    foods = Food.objects.all()

    

    # Show 4 food items per page
    page = request.GET.get('page', 1)
    paginator = Paginator(foods, 4)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    return render(request, 'food_list.html', {
       
        'foods': foods,
        'pages': pages,
        'title': 'Food List'
    })

@login_required(login_url='/loginn/')
 
def food_details_view(request, food_id):
    
    food = Food.objects.get(id=food_id)

    return render(request, 'food.html', {
        
        'food': food,
        
    })

@login_required(login_url='/loginn/')
 
def plan(request):
    if request.method == 'POST':
        # Get user input from the form
        current_weight = float(request.POST.get('current', 0))
        target_weight = float(request.POST.get('desired', 0))
        duration_needed = int(request.POST.get('time', 0))
        weeks = list(range(1, duration_needed + 1))
        weights = [current_weight + (target_weight - current_weight) * (week / duration_needed) for week in weeks]
        total_weight_gain = target_weight - current_weight
        target_rate = total_weight_gain / duration_needed 
        daily_caloric_intake = total_weight_gain * 7700 / (duration_needed * 7)
        plan=Plan.objects.create(user=request.user,current_weight=current_weight,target_weight=target_weight,target_duration=duration_needed,calorie_needed=round(daily_caloric_intake,2),target_rate=target_rate)
        print(weeks,weights)
        # Prepare data for JSON response
        weeks_json = json.dumps(weeks)
        weights_json = json.dumps(weights)
        data = {
            'weeks_json': weeks_json,
            'weights_json': weights_json,
            'plan':plan
        }
        

        return render(request,'plan.html',data)
    # plan=[]
    try:
        plan = Plan.objects.filter(user=request.user).latest('id')
        weeks = list(range(1, plan.target_duration + 1))
        weights = [plan.current_weight + (plan.target_weight - plan.current_weight) * (week / plan.target_duration) for week in weeks]
        weeks_json = json.dumps(weeks)
        weights_json = json.dumps(weights)
        return render(request, 'plan.html',{'weeks_json': weeks_json,
            'weights_json': weights_json,'plan':plan})
    except Plan.DoesNotExist:
    # Handle the case where the plan does not exist
        pass
    # if plan.exists() == True:
    #     weeks = list(range(1, plan.target_duration + 1))
    #     weights = [plan.current_weight + (plan.target_weight - plan.current_weight) * (week / plan.target_duration) for week in weeks]
    #     weeks_json = json.dumps(weeks)
    #     weights_json = json.dumps(weights)
    return render(request, 'plan.html')
@login_required(login_url='/loginn/')
 
def search(request):
    if request.method=="GET":
        query=request.GET.get('query')
        print(query)
        foods=Food.objects.all().filter(food_name__icontains=query)
        # unique_foods = {food.food_name: food for food in foods}.values()

        print(foods)
        if foods.exists() == False:
           
            api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
            
            response = requests.get(api_url, headers={'X-Api-Key': 'n3P1BNiUUGUMiYKsI+AOnw==MjowgehwIMMHfgRM'})
            
            if response.status_code == requests.codes.ok:
                data=response.json()
                if not data:
                    messages.error(request, 'Sorry,Not Found any matching food item!!!!')
                    return render(request,'food_list.html')

                
            else:
                print("hii")
                print("Error:", response.status_code, response.text)
                
            print(data)
            if data:
                    food_objects = []
                    
                    for food_data in data:
                        # Extract relevant information
                        food_name = food_data['name']
                        serving_size = food_data['serving_size_g']
                        calories = food_data['calories']
                        fat = food_data['fat_total_g']
                        protein = food_data['protein_g']
                        carbohydrates = food_data['carbohydrates_total_g']
                        fiber = food_data['fiber_g']
                        sugar = food_data['sugar_g']
                        cholestrol = food_data['cholesterol_mg']

                        # Create Food objects and add them to the list
                        food_objects.append(Food(
                            food_name=food_name,
                            calories=calories,
                            serving_size=serving_size,
                            fat=fat,
                            protein=protein,
                            carbohydrates=carbohydrates,
                            fiber=fiber,
                            sugar=sugar,
                            cholestrol=cholestrol
                        ))

                    # Bulk create Food objects to improve performance
                    Food.objects.bulk_create(food_objects)

                    # Query the newly created Food objects
                    foods = Food.objects.filter(food_name__icontains=query)
            
        page = request.GET.get('page', 1)
        paginator = Paginator(foods, 4)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        
        return render(request, 'food_list.html', {
            
            'foods': foods,
            'pages': pages,
            'title': 'Food List'
        })
    

def progress(request):
    user_weights = Weight.objects.filter(user=request.user).order_by('date')
    user_plan = Plan.objects.filter(user=request.user).latest('id')
    print(user_plan)
    weight_dates = [weight.date for weight in user_weights]
    weight_values = [weight.weight for weight in user_weights]

    # Calculate the target weight values based on the target duration in weeks
    target_weight_values = [
        user_plan.current_weight + user_plan.target_rate * i * 7  / user_plan.target_duration # Multiply by 7 to convert weeks to days
        for i in range(user_plan.target_duration * 7 + 1)  # Multiply by 7 to convert weeks to days
    ]
    print(target_weight_values)
    target_weight_dates = [
        user_plan.created_at + timezone.timedelta(days=i)
        for i in range(user_plan.target_duration * 7 + 1)  # Multiply by 7 to convert weeks to days
    ]

    # Ensure that the target weight arrays have the same length as the actual weight arrays
    target_weight_values = target_weight_values[:len(weight_values)]
    target_weight_dates = target_weight_dates[:len(weight_dates)]

    # Create the plot
    # Create the plot with a specified background color
    # Create the plot with a specified background color
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.set_facecolor('#191c24')
    ax.set_facecolor('#191c24')

    plt.plot(weight_dates, weight_values, label='Actual Weight', marker='o', linestyle='-', color='#0090e7')
    plt.plot(target_weight_dates, target_weight_values, label='Target Weight', marker='o', linestyle='-', color='#ffab00')
    plt.xlabel('Date')
    plt.ylabel('Weight')
    # plt.title('Weight Comparison Chart')
    plt.legend()

    # Set the text color to white
    plt.xticks(color='white')
    plt.yticks(color='white')

    # Set the legend text color to white
    # legend = plt.legend()
    # for text in legend.get_texts():
    #     text.set_color('white')

    # Set the color of the axis labels
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')

    # Convert the plot to a base64-encoded image
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0.1)
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    # Pass the base64-encoded image to the template
    context = {'graphic': graphic}





    return render(request,'progress.html',context)

