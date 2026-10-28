from django.shortcuts import render, redirect, get_object_or_404
from .models import *

def home(request):
    user_id = request.session.get("user_id")
    try:
        if user_id:
            user_name = users.objects.filter(id=user_id).first()
        return render(request, "landing.html", context={'user_name': user_name.username})
    except:
        return render(request, "landing.html")


def register(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        password_confirm = request.POST.get("password_confirm", "")

        if not email or not username or not password:
            return render(request, "register.html", {
                "error": "Please fill in all fields."
            })

        if password != password_confirm:
            return render(request, "register.html", {
                "error": "Passwords do not match."
            })

        if users.objects.filter(email__iexact=email).exists():
            return render(request, "register.html", {
                "error": "An account with this email already exists."
            })

        users.objects.create(
            email=email,
            username=username,
            password=password,
        )

        return redirect("tasks")

    return render(request, "register.html")


def login(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        user = users.objects.filter(email__iexact=email).first()

        if user and user.password == password:
            request.session["user_id"] = user.id
            return redirect("tasks")

        return render(request, "login.html", {
            "error": "Invalid email or password."
        })

    return render(request, "login.html")

def logout(request):
    request.session.flush()
    return redirect("home")


def tasks_page(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    user_name = users.objects.filter(id=user_id).first()

    current_user = get_object_or_404(users, id=user_id)
    tasks = Task.objects.filter(user=current_user).order_by(
        "completed", "-created_at"
    )

    return render(request, "tasks.html", {
        "user_name": user_name.username,
        "logged_in_user": current_user,
        "tasks": tasks,
        "total_count": tasks.count(),
        "completed_count": tasks.filter(completed=True).count(),
        "pending_count": tasks.filter(completed=False).count(),
    })


def add_task(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    if request.method == "POST":
        title = request.POST.get("title", "").strip()

        if title:
            current_user = get_object_or_404(users, id=user_id)
            Task.objects.create(user=current_user, title=title)

    return redirect("tasks")


def toggle_task(request, task_id):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    if request.method == "POST":
        task = get_object_or_404(Task, id=task_id, user_id=user_id)
        task.completed = not task.completed
        task.save(update_fields=["completed"])

    return redirect("tasks")


def delete_task(request, task_id):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    if request.method == "POST":
        task = get_object_or_404(Task, id=task_id, user_id=user_id)
        task.delete()

    return redirect("tasks")

