from pathlib import Path
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MyUser
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
import pandas as pd
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
import json
from stable_baselines3 import A2C
from stable_baselines3.common.vec_env import DummyVecEnv
from .venv import ModulePlanningenv  



def index(request):
    messages.success(request, "Welcome to the site!")
    return render(request,'index.html')

def login_request(request):
    if request.method == 'POST':
        
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                
                if user.usertype == 'superuser':
                    return redirect('superuser_dashboard')
                elif user.usertype == 'admin':
                    return redirect('admin_dashboard')
                else:
                    return redirect('user_dashboard')
            else:
                messages.error(request, "Invalid username or password.")
                form = LoginForm(request.POST)
        else:
            messages.error(request, "Form is invalid. Please check the errors below.")

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You've been registered successfully, now you can log in.")
            return redirect('login')
    else:
        form = RegisterForm()
    
    return render(request, 'signup.html', {'form': form})

def create_adm(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You have registered successfully")
            return redirect('login')
    else:
        form = RegisterForm()
        
    return render(request, 'adminform.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You were logged out. See you soon!")
    return redirect('login')

@login_required
def superuser_dashboard(request):
    return render(request, 'superuser.html', {'username': request.user.username})

@login_required
def admin_dashboard(request):
    return render(request, 'admin.html', {'username': request.user.username})

@login_required
def user_dashboard(request):
    return render(request, 'user.html', {'username': request.user.username})

def next1(request):
    file_path = Path(settings.MEDIA_ROOT) / 'demo data.xlsx'
    
    
    

    if file_path.exists():
        try:
            df = pd.read_excel(file_path)
            df.fillna('', inplace=True)
            df_table = df[['Bundle event', 'Modules Done']]
            table_html = df_table.to_html(classes='table table-striped', index=False)
            return render(request, 'next1.html', {'table_html': table_html})
        except Exception as e:
            print(f"Error reading the file: {e}")
            return render(request, 'next1.html', {'error': 'Error reading the file'})
    else:
        return render(request, 'next1.html', {'error': 'File not found'})
    
def next2(request):
    
    present_module_df = get_data()
    combined_table = present_module_df.to_html(classes='table table-striped', index=False)
    
    
    return render(request, 'next2.html', {'combined_table': combined_table})

def clean_breaks(str1):
    
    str1 = str1.split(",")
    str1 = [i for i in str1 if i != "BRK" and i != "BREAK"]
    return ",".join(str1)

def get_data():
    
    file_path = Path(settings.MEDIA_ROOT) / 'demo data.xlsx'
    
    
    df = pd.read_excel(file_path)
    
    
    df.fillna('', inplace=True)
    
    
    df['Module Done and Present Batch'] = df['Modules Done'].astype(str) + ',' + df['Present Module '].astype(str)
   
    
    present_module_df = df[['Module Done and Present Batch', 'Time to finish the module']]
    
    
    present_module_df['Module Done and Present Batch'] = [clean_breaks(i) for i in present_module_df['Module Done and Present Batch']]
    
    return present_module_df




from django.shortcuts import render
import pandas as pd
import json
from stable_baselines3 import A2C
from stable_baselines3.common.vec_env import DummyVecEnv


from .venv import ModulePlanningenv  


def plans(request):
    file_path = Path(settings.MEDIA_ROOT) / 'demo data.xlsx'
   
    batches = get_data()['Module Done and Present Batch'].to_list()
    batches1 = [encode(i) for i in batches]
    
   
    env = ModulePlanningenv(batches1)
    env1 = DummyVecEnv([lambda: env])
    model = A2C("MlpPolicy", env1, verbose=2)
    model.learn(total_timesteps=10000)
    
    
    res = model.predict(env.get_initial_state())
    res = list(res[0])
    result = env.step(res)

    if result[1] > 0:
       
        modules = get_modules(res)
        df = pd.read_excel(file_path)
        df = df['Bundle event'].to_list()

        d = pd.DataFrame({
            "Batches": df,
            "Modules Done": batches,
            "Planned Module": modules
        })
        table_html = d.to_html(classes='table table-striped', index=False)
        
        
        return render(request, 'demo.html', {'res': table_html})
    else:
        
        return render(request, 'demo1.html')

def get_modules(res):
    with open("inverse.json", "r") as f:
        m = json.load(f)
    r = [m[str(i)] for i in res]
    return r

def encode(str1):
    str1 = str1.split(",")
    str1 = [i.strip() for i in str1]
    with open("mod.json", "r") as f:
        d = json.load(f)
    str1 = [d[i] for i in str1 if i in d.keys()]
    return str1

