from django.http import JsonResponse
from pustakalaya_apps.document.models import Document
from pustakalaya_apps.audio.models import Audio
from pustakalaya_apps.video.models import Video

# Create your views here.


def set_featured_view(request):
    # 1. Send the ajax request. not submit request.
    # 2. grab the data here.
    # 3. set the review for the requested doc with respective user
    # 4. return the ajax response.
    if request.method == "POST":
        data = request.POST["input"]
        content_id = request.POST["content_id"]
        content_type = request.POST["content_type"]

        if request.user.is_authenticated:
            if data is not None and content_type is not None and content_id is not None:
                if content_type == "document":
                    p = Document.objects.get(id=content_id)
                    print("docuemt p",p)
                    # document
                    pass
                elif content_type == "audio":
                    p = Audio.objects.get(id=content_id)
                    print("audio p",p)

                    # audio
                    pass
                else:
                    p = Video.objects.get(id=content_id)
                    print("video p",p)

                    # video
                    pass

                p.featured = "yes"
                p.save()
                print("save complete")
                return JsonResponse({'response': data, "content_id": content_id, "content_type": content_type,"pk_value":p.pk})
            else:
                return JsonResponse({'response':data,"content_id":content_id,"content_type":content_type})
        else:
            return JsonResponse({'response':"user_not_logged_in","content_id":content_id,"content_type":content_type})

        return JsonResponse({'response': data,"content_id":content_id,"content_type":content_type})

    return JsonResponse({'response':'Favourite Collection'})


def unset_featured_view(request):

    if request.method == "POST":
        data = request.POST["input"]
        content_id = request.POST["content_id"]
        content_type = request.POST["content_type"]

        if request.user.is_authenticated:

            if data is not None and content_type is not None and content_id is not None:

                if content_type == "document":
                    p = Document.objects.get(id=content_id)
                    # document
                    pass
                elif content_type == "audio":
                    p = Audio.objects.get(id=content_id)
                    # audio
                    pass
                else:
                    p = Video.objects.get(id=content_id)
                    # video
                    pass

                p.featured = "no"
                p.save()

                return JsonResponse({'response': data, "content_id": content_id, "content_type": content_type,"pk_value":p.pk })
            else:
                return JsonResponse({'response':data,"content_id":content_id,"content_type":content_type})
        else:
            return JsonResponse({'response':"user_not_logged_in","content_id":content_id,"content_type":content_type})

        return JsonResponse({'response': data,"content_id":content_id,"content_type":content_type})

    return JsonResponse({'response':'Featured unset complete'})


