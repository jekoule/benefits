from django.contrib.auth import get_user_model
from members.models import Member
import hashlib
import random
from django.core.mail import send_mail
from django.urls import reverse
User = get_user_model()


def create_member(email, company):
    # Create user account for member with random password
    user = User(email=email, is_active=False)
    password = User.objects.make_random_password()
    user.set_password(password)
    user.save()
    # Generating activation key
    # First generate random part as a result of hashing random string
    random_part = hashlib.sha256(str(random.random())).hexdigest()[:5]
    hashable = random_part + user.email.encode('utf-8')
    # Then create hash for random_part and email
    activation_token = hashlib.sha256(hashable).hexdigest()
    # then create member itself
    member = Member(
        user=user,
        company=company,
        activation_token=activation_token)
    member.save()
    # Finally send an email to member with an invitation to activate account
    activation_link = reverse(
        'customer.views.activate',
        kwargs={'user_id': user.pk, 'token': activation_token}
    )
    send_mail(
        'Активация аккаунта Benefits',
        activation_link,
        'noreply@benefits.kz',
        user.email
    )
