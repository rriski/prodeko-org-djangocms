import json
import os
from io import BytesIO

from django.conf import settings
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.exceptions import PermissionDenied
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.http import (Http404, HttpResponse, HttpResponseForbidden,
                         HttpResponseRedirect, JsonResponse)
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView, UpdateView
from PIL import Image

from .forms import EhdokasForm, KysymysForm, VastausForm
from .models import Ehdokas, Kysymys, Vastaus, Virka


class EhdokasDeleteView(SuccessMessageMixin, DeleteView):
    """ Handles 'Ehdokas' model application deleting.

    Raises:
        PermissionDenied: Unauthorized user tried to delete an application that
                          they didn't create.
    """
    model = Ehdokas
    success_url = reverse_lazy('app_vaalit:vaalit')
    success_message = "%(name)s poistettu onnistuneesti."

    def get_object(self, *args, **kwargs):
        """Allow updating the object only if request.user created the application."""
        obj = super(EhdokasDeleteView, self).get_object(*args, **kwargs)
        if obj.auth_prodeko_user != self.request.user:
            raise PermissionDenied
        return obj

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(EhdokasDeleteView, self).delete(request, *args, **kwargs)


class EhdokasUpdateView(UpdateView):
    """ Handles 'Ehdokas' model application updates.

    Raises:
        PermissionDenied: Unauthorized user tried to delete an application that
                          they didn't create.
    """
    model = Ehdokas
    form_class = EhdokasForm
    success_url = reverse_lazy('app_vaalit:vaalit')
    template_name = 'vaalit_modify_application.html'

    def get_object(self, *args, **kwargs):
        """Allows updating the object only if request.user created the application."""
        obj = super(EhdokasUpdateView, self).get_object(*args, **kwargs)
        if obj.auth_prodeko_user != self.request.user:
            raise PermissionDenied
        return obj

    def form_valid(self, form, *args, **kwargs):
        request = self.request
        context = self.get_context_data()
        ehdokas = self.get_object()
        response = handle_modify_ehdokas(request, context=context, ehdokas=ehdokas)
        return HttpResponseRedirect(self.get_success_url())


def delete_kysymys_view(request, pk):
    """Handle question deletions."""
    kysymys = get_object_or_404(Kysymys, pk=pk)
    if kysymys.created_by != request.user:
        raise PermissionDenied
    if request.method == 'POST' and request.is_ajax():
        id = kysymys.id
        kysymys.delete()
        return JsonResponse({'delete_kysymys_id': id})
    else:
        raise Http404


def update_kysymys_view(request, pk):
    """Handle question deletions."""
    kysymys = get_object_or_404(Kysymys, pk=pk)
    if kysymys.created_by != request.user:
        raise PermissionDenied
    if request.method == 'POST':
        kysymys.delete()
        return redirect('/vaalit')
    else:
        raise Http404


def crop_pic(uploaded_img, x, y, w, h):
    if not uploaded_img:
        img_url_prt = static('images/misc/anonymous_prodeko.jpg')
        x, y, w, h = 0, 0, 150, 150
        img_url_full = settings.BASE_DIR + '/prodekoorg' + img_url_prt
        img = Image.open(img_url_full)
    else:
        img = Image.open(uploaded_img.file)
    area = (x, y, x + w, y + h)
    cropped_img = img.crop(area)
    img_io = BytesIO()
    # Have to use because people might upload them anyways...
    # We get an error if forma='JPEG' because png's have alpha channel
    cropped_img.save(fp=img_io, format='PNG')
    buff_val = img_io.getvalue()
    contentFile = ContentFile(buff_val)
    # If no image was provided use anonymous_prodeko.jpg
    name = uploaded_img.name if uploaded_img else 'anonymous_prodeko.jpg'
    ret = InMemoryUploadedFile(contentFile, None, name,
                               'image/png', cropped_img.tell, None)
    img.close()
    img_io.close()
    return ret


def get_hidden_inputs(post):
    hidden_virka = post.get("hidden-input-virka")
    x = float(post.get("hidden-crop-x"))
    y = float(post.get("hidden-crop-y"))
    w = float(post.get("hidden-crop-w"))
    h = float(post.get("hidden-crop-h"))
    return hidden_virka, x, y, w, h


def is_duplicate_application(request, hidden_virka):
    # If the user has already applied to this virka
    # don't create a new ehdokas instance and display a warning message
    if Ehdokas.objects.filter(virka__name=hidden_virka, auth_prodeko_user=request.user).exists():
        messages.warning(request, 'Et voi hakea samaan virkaan kahta kertaa, muokkaa edellistä hakemustasi.')
        return True
    else:
        return False


def get_ehdokkaat_json(context, ehdokas):
    # Append the new ehdokas to the ehdokas_json list that is processed in javascript
    ehdokas_new_python = serialize('python', [ehdokas], use_natural_foreign_keys=True,
                                   fields=('auth_prodeko_user', 'virka'))
    ehdokas_new_json = json.dumps([d['fields'] for d in ehdokas_new_python])
    ehdokas_new = json.loads(ehdokas_new_json)
    ehdokkaat_json = json.loads(context['ehdokkaat_json'])
    ehdokkaat_json.extend(ehdokas_new)  # Extend operates in-place and returns none
    return json.dumps(ehdokkaat_json)


def handle_submit_ehdokas(request, context):
    form_ehdokas = EhdokasForm(request.POST, request.FILES)
    # Store the form in context in case there were errors
    context['form_ehdokas'] = form_ehdokas

    if form_ehdokas.is_valid():

        # Get hidden input values from POST
        hidden_virka, x, y, w, h = get_hidden_inputs(request.POST)

        # Check for duplicate application to one Virka by the same Ehdokas
        if is_duplicate_application(request, hidden_virka):
            return redirect('/vaalit')

        # Crop the image using the hidden input x, y, w and h coordinates
        cropped_pic = crop_pic(request.FILES.get('pic', ), x, y, w, h)

        # Get the ehdokas object without committing changes to the database.
        # We still need to append pic, user object and foreign key virka object to the ehdokas object.
        ehdokas = form_ehdokas.save(commit=False)
        ehdokas.pic = cropped_pic
        ehdokas.auth_prodeko_user = request.user
        ehdokas.virka = get_object_or_404(Virka, name=hidden_virka)
        ehdokas.save()

        context['ehdokkaat_json'] = get_ehdokkaat_json(context, ehdokas)
        context['form_ehdokas'] = form_ehdokas
        return render(request, 'vaalit.html', context)
    else:
        # If there are errors show the form by setting it's display to 'block'
        context['style_vaaliApplyForm'] = 'display: block;'
        # Return the form with error messages and reder vaalit main page
        return render(request, 'vaalit.html', context)


def handle_modify_ehdokas(request, context, ehdokas):
    # Get hidden input values from POST
    hidden_virka, x, y, w, h = get_hidden_inputs(request.POST)

    # Crop the image using the hidden input x, y, w and h coordinates
    cropped_pic = crop_pic(request.FILES.get('pic', ), x, y, w, h)

    # Get the ehdokas object without committing changes to the database.
    # We still need to append pic, user object and foreign key virka object to the ehdokas object.
    # TODO handle name once auth_prodeko is ready
    ehdokas.pic = cropped_pic
    ehdokas.introduction = request.POST.get('introduction', )
    ehdokas.virka = get_object_or_404(Virka, name=hidden_virka)
    ehdokas.save()
    render(request, 'vaalit.html', context)


def handle_submit_kysymys(request, context):
    """Process posted questions.

    Returns:

    """
    form_kysymys = KysymysForm(request.POST)
    hidden_virka = request.POST.get("hidden-input-virka")

    # Form validation
    if form_kysymys.is_valid():
        kysymys = form_kysymys.save(commit=False)
        if request.user.is_anonymous():
            kysymys_created_by = None
        else:
            kysymys.created_by = request.user

        virka = get_object_or_404(Virka, name=hidden_virka)
        kysymys.to_virka = virka
        kysymys.save()

        context['kysymys'] = kysymys
        context['virka'] = virka
        html = render_to_string('vaalit_question.html', context, request)

        return HttpResponse(html)
    else:
        raise Http404


def handle_submit_answer(request, context):
    form_vastaus = VastausForm(request.POST)
    hidden_kysymys_id = request.POST.get("hidden-input-kysymys")

    # Form validation
    if form_vastaus.is_valid():
        vastaus = form_vastaus.save(commit=False)
        vastaus.by_ehdokas = get_object_or_404(Ehdokas, auth_prodeko_user=request.user)
        vastaus.to_question = get_object_or_404(Kysymys, id=hidden_kysymys_id)
        vastaus.save()

        html = render_to_string('vaalit_answer.html', context, request)

        #return HttpResponse(html)

        return redirect('/vaalit')
    else:
        print("went here")
        # Return form with error and render vaalit main page
        return render(request, 'vaalit.html', context)


def main_view(request):
    context = {}
    ehdokkaat = Ehdokas.objects.all()
    # ehdokkaat_json is parsed to JSON in the template 'vaalit_question_form.html'
    ehdokkaat_python = serialize('python', ehdokkaat, use_natural_foreign_keys=True,
                                 fields=('auth_prodeko_user', 'virka'))
    ehdokkaat_json = json.dumps([d['fields'] for d in ehdokkaat_python])
    context['virat'] = Virka.objects.all()
    context['ehdokkaat'] = ehdokkaat
    context['ehdokkaat_json'] = ehdokkaat_json
    context['count_ehdokkaat_hallitus'] = Virka.objects.filter(is_hallitus=True).count()
    context['count_ehdokkaat_toimarit'] = Virka.objects.filter(is_hallitus=False).count()
    print(request.POST)
    if request.method == 'POST':
        if 'submitVirka' in request.POST:
            return handle_submit_ehdokas(request, context)
        elif 'submitVastaus' in request.POST:
            return handle_submit_answer(request, context)
        elif 'submitKysymys' in request.POST and request.is_ajax():
            return handle_submit_kysymys(request, context)
        else:
            raise Http404
    else:
        context['form_ehdokas'] = EhdokasForm()
        return render(request, 'vaalit.html', context)