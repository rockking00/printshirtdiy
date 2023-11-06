from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django_ratelimit.decorators import ratelimit
from django.http import HttpResponseBadRequest, JsonResponse
from django.core.cache import cache
from openai.error import OpenAIError
import openai
import json


# api_key = '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'
from django.conf import settings
openai.api_key = settings.OPENAI_API_KEY


@ratelimit(key='ip', rate='3/d', method='POST', block=True)
@csrf_exempt
def create(request):
    default_image = "/static/demo/img.svg"
    try:
        if request.method == 'POST':
            prompt = request.POST.get('prompt')
            images = generate(prompt)
            image_src = json.dumps(images)
            post_count = cache.get_or_set('post_count', 0, 86400)
            if post_count is None:
                post_count = 0
            cache.set('post_count', post_count + 1, 86400)
            return render(request, 'demo/create.html', {'images':images, 'default_image': default_image, 'image_src': image_src, 'post_count': post_count + 1})
        else:
            post_count = cache.get('post_count', 0)
            return render(request, 'demo/create.html', {'default_image': default_image, 'post_count': post_count})
    except OpenAIError:
        return HttpResponseBadRequest('Request timed out'
                                      'Return to <a href="/create/">create</a> page')


def generate(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=4,
        size="1024x1024",
        api_key=api_key
    )
    images = []
    for image_url in response['data']:
        img_data = image_url['url']
        images.append(img_data)
    return images

