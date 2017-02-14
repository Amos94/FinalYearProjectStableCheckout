from django import forms

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
