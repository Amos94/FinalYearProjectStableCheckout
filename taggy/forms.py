from django import forms

from taggy.modules.Queries import Queries


class CreateSet(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CreateSet, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            if (field == 'setname'):
                placeholder = 'Set name'
            elif(field == 'setdescr'):
                placeholder = 'Set description'
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'style':'width:50%;',
                'placeholder':placeholder
            })
    setname = forms.CharField(label='New set name')
    setdescr = forms.CharField(label = 'New set description')

class UpdateSet(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UpdateSet, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            if (field == 'updateset'):
                placeholder = 'Set'
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'style': 'width:50%;',
                'placeholder': placeholder
            })

    updateset = forms.Textarea()

class DeleteSet(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UpdateSet, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            if (field == 'updateset'):
                placeholder = 'Set'
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'style': 'width:50%;',
                'placeholder': placeholder
            })

    updateset = forms.Textarea()

class ChooseTag(forms.Form):
    CHOICES = {}
    qryObject = Queries()
    results = []
    # results = qryObject.getTagAndPOR()
    # for result in results:
    #     CHOICES[result[0]] = (result[1], result[2])

    field = forms.ChoiceField(choices=CHOICES, required=True, label='Choose Tag')
    def __init__(self, *args, **kwargs):
        super(ChooseTag, self).__init__(*args, **kwargs)

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file'
    )


class CreateDomain(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CreateDomain, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            if (field == 'domainname'):
                placeholder = 'Domain name'
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'style':'width:50%;',
                'placeholder':placeholder
            })
    domainname = forms.CharField(label='New domain name')



class CreateTag(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CreateTag, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            if (field == 'tagname'):
                placeholder = 'Tag name'
            if (field == 'tagdescr'):
                placeholder = 'Tag description'
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'style':'width:50%;',
                'placeholder':placeholder
            })
    tagname = forms.CharField(label='Tag Name')
    tagdescr = forms.CharField(label='Tag Description')


class EditDomain(forms.Form):
    def __init__(self, *args, **kwargs):
        super(EditDomain, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            if (field == 'domainname'):
                placeholder = 'Domain name'
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'style':'width:50%;',
                'placeholder':placeholder
            })
    domainname = forms.CharField(label='New domain name')


class FinalizePost(forms.Form):
    def __init__(self, *args, **kwargs):
        super(FinalizePost, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'style':'width:10%;',
            })
    postId = forms.CharField(disabled=True)