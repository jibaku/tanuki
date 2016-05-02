"""Dynamic forms created from DB data."""
import logging
import uuid

from django import forms
from django.core.urlresolvers import reverse
from django.forms import models
from django.utils.safestring import mark_safe

from survey.models import (AnswerInteger, AnswerRadio, AnswerSelect,
                           AnswerSelectMultiple, AnswerText, Question,
                           Response)
from survey.signals import survey_completed
from survey.utils import get_choices
from survey.widgets import ImageSelectWidget


class HorizontalRadioRenderer(forms.RadioSelect.renderer):
    """FormRendered to have radio button horizontaly rather than verticaly."""

    def render(self):
        """Render content."""
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


class ResponseForm(models.ModelForm):
    """Form to handle user response."""

    class Meta:
        model = Response
        fields = ()

    def __init__(self, *args, **kwargs):
        """A survey object need to be passed as the survey kwargs."""
        empty_tuple = ('', '-------------')
        survey = kwargs.pop('survey')
        self.survey = survey
        self.user = kwargs.pop('user')
        self.separator = self.survey.separator
        self.callback_code = kwargs.pop('callback_code', None)
        try:
            self.step = int(kwargs.pop('step'))
        except KeyError:
            self.step = None

        super(ResponseForm, self).__init__(*args, **kwargs)
        random_uuid = uuid.uuid4().hex
        self.uuid = random_uuid
        self.fields['tanuki_callback_code'] = forms.CharField(
            widget=forms.HiddenInput, required=False
        )
        self.fields['tanuki_callback_code'].initial = self.callback_code
        self.steps_count = survey.questions().count()
        # add a field for each survey question, corresponding to the question
        # type as appropriate.
        data = kwargs.get('data')
        for index, q in enumerate(survey.questions()):
            if (self.survey.display_by_question and
               index != self.step and self.step is not None):
                continue
            else:
                field_name = "question_%d" % q.pk
                if q.question_type == Question.TEXT:
                    self.fields[field_name] = forms.CharField(
                        label=q.text,
                        widget=forms.Textarea
                    )
                elif q.question_type == Question.SHORT_TEXT:
                    self.fields[field_name] = forms.CharField(
                        label=q.text,
                        widget=forms.TextInput
                    )
                elif q.question_type == Question.RADIO:
                    question_choices = get_choices(q.choices,
                                                   separator=self.separator)
                    self.fields[field_name] = forms.ChoiceField(
                        label=q.text,
                        widget=forms.RadioSelect(
                            renderer=HorizontalRadioRenderer
                        ),
                        choices=question_choices
                    )
                elif q.question_type == Question.SELECT:
                    question_choices = get_choices(q.choices,
                                                   separator=self.separator)
                    # add an empty option at the top so that the user has to
                    # explicitly select one of the options
                    question_choices = tuple([empty_tuple]) + question_choices
                    self.fields[field_name] = forms.ChoiceField(
                        label=q.text,
                        widget=forms.Select,
                        choices=question_choices
                    )
                elif q.question_type == Question.SELECT_IMAGE:
                    question_choices = get_choices(q.choices,
                                                   separator=self.separator)
                    # add an empty option at the top so that the user has to
                    # explicitly select one of the options
                    question_choices = tuple([empty_tuple]) + question_choices
                    self.fields[field_name] = forms.ChoiceField(
                        label=q.text,
                        widget=ImageSelectWidget,
                        choices=question_choices
                    )
                elif q.question_type == Question.SELECT_MULTIPLE:
                    question_choices = get_choices(q.choices,
                                                   separator=self.separator)
                    self.fields[field_name] = forms.MultipleChoiceField(
                        label=q.text,
                        widget=forms.CheckboxSelectMultiple,
                        choices=question_choices
                    )
                elif q.question_type == Question.INTEGER:
                    self.fields[field_name] = forms.IntegerField(label=q.text)
                # if the field is required, give it a corresponding css class.
                if q.required:
                    self.fields[field_name].required = True
                    self.fields[field_name].widget.attrs["class"] = "required"
                    self.fields[field_name].widget.attrs["required"] = True
                else:
                    self.fields[field_name].required = False
                # add the category as a css class, and add it as a data
                # attribute as well (this is used in the template to allow
                # sorting the questions by category)
                if q.category:
                    cat_name = q.category.name
                    classes = self.fields[field_name].widget.attrs.get("class")
                    category_class = " cat_%s" % q.category.name
                    if classes:
                        new_classes = classes + (category_class)
                    else:
                        new_classes = (category_class)
                    self.fields[field_name].widget.attrs["class"] = new_classes
                    self.fields[field_name].widget.attrs["category"] = cat_name

                classes = self.fields[field_name].widget.attrs.get("class")
                if q.question_type == Question.SELECT:
                    new_classes = classes + (" cs-select cs-skin-boxes")
                elif q.question_type == Question.RADIO:
                    new_classes = classes + (
                        " fs-radio-group fs-radio-custom clearfix")
                # elif q.question_type == Question.SELECT_MULTIPLE:
                #    new_classes = classes + (" ")
                self.fields[field_name].widget.attrs["class"] = new_classes

                # initialize the form field with values from a POST request, if
                # any.
                if data:
                    self.fields[field_name].initial = data.get(field_name)

    def has_next_step(self):
        """Check if the form has a next step."""
        if self.survey.display_by_question:
            if self.step < (self.steps_count - 1):
                return True
        return False

    def next_step_url(self):
        """Return the url for the next step."""
        if self.has_next_step():
            return reverse('survey-detail-step',
                           kwargs={
                               'id': self.survey.id,
                               'step': self.step + 1
                           })
        else:
            return None

    def current_step_url(self):
        """Return the url for the current step."""
        return reverse('survey-detail-step',
                       kwargs={
                           'id': self.survey.id,
                           'step': self.step
                       })

    def save(self, commit=True):
        """
        save the response object
        """
        response = super(ResponseForm, self).save(commit=False)
        response.survey = self.survey
        response.interview_uuid = self.uuid
        if self.user.is_authenticated():
            response.user = self.user
        response.save()

        # response "raw" data as dict (for signal)
        data = {
            'survey_id': response.survey.id,
            'interview_uuid': response.interview_uuid,
            'callback_code': self.callback_code,
            'responses': []
        }
        # create an answer object for each question and associate it with this
        # response.
        for field_name, field_value in self.cleaned_data.iteritems():
            if field_name.startswith("question_"):
                # warning: this way of extracting the id is very fragile and
                # entirely dependent on the way the question_id is encoded in
                # the field name in the __init__ method of this form class.
                q_id = int(field_name.split("_")[1])
                q = Question.objects.get(pk=q_id)

                if q.question_type in [Question.TEXT, Question.SHORT_TEXT]:
                    a = AnswerText(question=q)
                    a.body = field_value
                elif q.question_type == Question.RADIO:
                    a = AnswerRadio(question=q)
                    a.body = field_value
                elif q.question_type == Question.SELECT:
                    a = AnswerSelect(question=q)
                    a.body = field_value
                elif q.question_type == Question.SELECT_IMAGE:
                    a = AnswerSelect(question=q)
                    value, img_src = field_value.split(":", 1)
                    a.body = value
                elif q.question_type == Question.SELECT_MULTIPLE:
                    a = AnswerSelectMultiple(question=q)
                    a.body = field_value
                elif q.question_type == Question.INTEGER:
                    a = AnswerInteger(question=q)
                    a.body = field_value
                data['responses'].append((a.question.id, a.body))
                # Some debug info
                msg = "creating answer to question %d of type %s" % (
                    q_id, a.question.question_type
                )
                logging.debug(msg)
                logging.debug(a.question.text)
                logging.debug('answer value:')
                logging.debug(field_value)

                a.response = response
                a.save()
        survey_completed.send(sender=Response, instance=response, data=data)
        return response
