

# def users(request):
#     users_list = User.objects.all()
#     return render(request, 'login.html', {'users': users_list, 'title': 'Users'})





# def user_view(request, user_id: int = None, slug: str = None):
#     # if user_id:
#     #     user = get_object_or_404(User, pk=user_id)
#     # else:
#     user = get_object_or_404(User, slug=slug)
#
#     return render(request, 'user.html', {'user': user, 'title': user.name})



# def create_user(request):
#     if request.method == 'POST':
#         form = CreateUserForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('users')
#     else:
#         form = CreateUserForm()
#     return render(request, 'users/register.html', {'form': form, 'title': 'Create User'})
