import logging

from django.shortcuts import render
from .forms import AppForm
from .models import FormUser
from django.contrib import messages
from django.core.mail import EmailMessage

logger = logging.getLogger(__name__)


def index(request):
    if request.method == 'POST':
        logger.info("POST request received on index view")
        logger.info("Raw POST data: %s", request.POST)

        form = AppForm(request.POST)

        if form.is_valid():
            logger.info("Form is valid, cleaned_data: %s", form.cleaned_data)

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            date = form.cleaned_data['date']
            occupation = form.cleaned_data['occupation']

            new_entry = FormUser.objects.create(first_name=first_name, last_name=last_name, email=email, date=date, occupation=occupation)
            logger.info("Saved to DB with id=%s", new_entry.id)

            message_body = f"a new job app was submitted. thank you! \n{first_name} {last_name}"
            email_message = EmailMessage("from submission confirmation", message_body, to=[email])
            try:
                email_message.send()
                logger.info("Confirmation email sent to %s", email)
            except Exception as e:
                logger.error("Failed to send email: %s", e)

            messages.success(request, 'Thank you for your message')
        else:
            logger.warning("Form is INVALID, errors: %s", form.errors)
    else:
        form = AppForm()

    return render(request, "index.html", {"form": form})