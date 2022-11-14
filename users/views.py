from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, MemberForm
from django.views.generic.list import ListView
from django.shortcuts import render
from users.models import CustomUser, Member
from diagram.models import Block
from diagram.models import Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required



def login_view(request):
    if request.user.is_authenticated:
        return redirect('index:dashboard')
    form = LoginForm(request.POST or None)

    msg = None
    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(username=email, password=password)
            if user:
                login(request, user)
                return redirect('index:dashboard')
            else:
                form.add_error('email', 'Email or Password is not correct')

    return render(request, "users/login.html", {"form": form})


class ContactListView(ListView):

    model = Member
    paginate_by = 9  # if pagination is desired
    template_name = 'users/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MemberForm()
        return context

    def post(self, request):
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.error(request,  'The Email field or Phone number field is not correct' )
            return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='users:login')
def mail_response_view(request, random_text):

    context = {'state': False}
    try:
        random_text = random_text.split('_')
        user_url, block_id = random_text[0:2]
        user = CustomUser.objects.get(rand_text=user_url)
        block = Block.objects.get(id=block_id, is_active=True)
    except:
        return render(request, 'users/email_response.html', context)

    for group in block.user_groups.all():
        for sub_users in group.user_set.all():
            if user == sub_users:
                context['state'] = True
                break
        if context['state']:
            break

    if not context['state']:
        return render(request, 'users/email_response.html', context)

    try:
        comment = Comment.objects.get(author=user, block=block, text='Email received')
    except Comment.DoesNotExist:
        comment = Comment(author=user, block=block, text='Email received', label='Email Notif')
        comment.save()
    context['state'] = True
    return render(request, 'users/email_response.html', context)


@login_required(login_url='users:login')
def sms_panel_view(request):
    context = {}
    saved_member_id = request.session.get("member_id")
    if saved_member_id:
        context['saved_member'] = Member.objects.filter(id=saved_member_id)
        context['saved_member_id'] = int(saved_member_id)
    members = Member.objects.all()
    context['members'] = members

    return render(request, 'users/send_message.html', context)


@login_required(login_url='users:login')
def save_member_session(request, member_id):
    request.session["member_id"] = member_id
    return redirect('users:sms-panel')