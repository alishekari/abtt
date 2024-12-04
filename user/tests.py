from user.models import User

User.objects.all().count()

User.objects.search(query=None).count()