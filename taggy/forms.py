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
