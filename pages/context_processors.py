from .models import GeneralInformation

def generalinformationgetter(request):
    phone = GeneralInformation.objects.filter(name='phone').first()
    facebook = GeneralInformation.objects.filter(name='facebook').first()
    location = GeneralInformation.objects.filter(name='location').first()
    email = GeneralInformation.objects.filter(name='email').first()
    return {
        'phone':phone.content,
        'facebook':facebook.content,
        'location':location.content,
        'email':email.content
        }
