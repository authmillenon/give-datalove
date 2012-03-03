from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext, ugettext_lazy as _
from give.models import *

class DataloveUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(DataloveUserChangeForm, self).__init__(*args,**kwargs)
        self.fields['username'].help_text = ''

    class Meta(UserChangeForm.Meta):
        fields = ('username','email',)

class BaseUserWebsiteFormSet(forms.models.BaseModelFormSet):
    def __init__(self, user, *args, **kwargs):
        super(BaseUserWebsiteFormSet, self).__init__(*args, **kwargs)
        self.user = user
        self.queryset = user.get_profile().websites.all()
        for form in self:
            form.fields['url'].widget.attrs['class'] = 'url_input'

    def save(self, *args, **kwargs):
        websites = super(BaseUserWebsiteFormSet,self).save(commit=False)
        for website in websites:
            if website.user_id == None:
                website.user = self.user.get_profile()
            website.save()

UserWebsiteFormSet = forms.models.modelformset_factory(
        UserWebsite,
        formset=BaseUserWebsiteFormSet,
        fields=('url',)
    )
