import warnings
warnings.filterwarnings('ignore', message='.*cryptography', )
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from .forms import *
from loguru import logger
# from django.http import JsonResponse
from django.utils.timezone import now
from django.conf import settings
from utils.weather_scrape import scraped_data
# from django.views.decorators.gzip import gzip_page
from datetime import datetime
from django.contrib import messages
import random
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
import requests
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
#----blog imports
from django.db.models import Q
from django.views.generic.edit import FormMixin
from django.views.generic.detail import DetailView
from django.views.generic import MonthArchiveView, ListView
from hitcount.views import HitCountDetailView

#---------cache decorator----------
from django.views.decorators.cache import cache_page
# -----------examples for using localized dae objects----------------
# localized_date = formats.date_format(date_obj, 'SHORT_DATE_FORMAT')
# localized_time = formats.time_format(time_obj, 'SHORT_TIME_FORMAT')
#----------generate unique code for email subscription conf--------------------
def random_digits():
    return "%0.12d" % random.randint(0, 999999999999)
#========================underconstruction home page=================================
# def underconstruction(request):
#     """
#     This view replaces the home page when website is under construction
#     """
#     template = 'services/underconstruction.html'
#     weather = scraped_data()
#     context = {
#         "weather": weather,
#     }
#     return render(request, template, context)
#========================map coming soon VIEW=================================

def map_coming_soon(request):
    template = "services/map-coming-soon.html"
    context = {}
    return render(request, template, context)

#========================add testimonial VIEW=================================
def add_testimonial(request):
    template = 'services/add_testimonial.html'
    form = CaptchaForm()
    if request.method=='POST':
        review_form = TestimonialForm(request.POST or None, request.FILES or None)
        try:
            if form.is_valid():
                if review_form.is_valid():
                    new_review = review_form.save(commit=False)
                    new_review.status = False
                    new_review.save()
                    messages.success(request, "Message send for approval.")
                    return redirect('home')
                else:
                    messages.error(request, "Please check for empty fields.")
                    return redirect('add_testimonial')
            else:
                messages.error(request, "Captcha incorrect.")
                return redirect('add_testimonial')
        except Exception as e:
            messages.error(request, "Please check for empty fields.")

    return render(request, template, {"form":form,"review_form":TestimonialForm()})
#========================add allowed vehicle VIEW=================================
# def allowed_vehicles(request):
#     template = 'services/allowed_vehicles.html'
#     allowed_vehicles = AllowedVehicles.objects.all()
#     context = {}
#     if request.method == "GET" and request.GET.get('form-type') == "search":
#         query = request.GET.get("q").replace(" ", "")
#         r = AllowedVehicles.objects.filter(Q(identification_nr=query)).values()
#         if r:
#             vehicle = r[0]
#             start_date = vehicle['start_date']
#             end_date = vehicle['end_date']
#             today = datetime.today().date()
#             if start_date > today:
#                 messages.warning(request, _('This car is not yet allowed in the park! Permit starts on {0}.').format(start_date))
#             elif end_date >= today:
#                 messages.success(request, _("This car is allowed in the park!"))
#                 context.update({"car_info":r, 'area':[i['name'] for i in AccessArea.objects.all().values() if i['id']==vehicle['area_id']][0]})
#             else:
#                 messages.warning(request, _("This car was previously authorized but permit is expired!"))
#         else:
#             messages.error(request, _("This car is not authorized!"))
#     else:
#         context = {}
#     return render(request, template, context)


#========================weatehr data page=================================
# async def weather_data(request):
#     # Fetch weather data asynchronously
#     weather = await scraped_data()
#     return JsonResponse(weather)
#========================home page=================================
@csrf_exempt
@cache_page(60 * 60)  # Cache for 60 minutes (in seconds)
def home(request):
    template = 'services/home.html'
    captcha_form = CaptchaForm()
    context = {
        "captcha_form": captcha_form
    }
    #handle post requests
    # if request.method == 'POST':
    #     form_type = request.POST.get('form-type')

    #     if form_type == "signin-form":
    #         handle_signin(request, context)
    #     elif form_type == "subscribe":
    #         handle_subscription(request, context)

    # Fetch weather data 
    weather = scraped_data()
    context['weather'] = weather
    # logger.debug(context['weather'])
    # Fetching data from the database and adding to context
    context.update({
        'attr_categ': AttractionCategory.objects.all(),
        'attractions': Attraction.objects.filter(featured=True),
        'current_date': datetime.today().date(),
        'reviews': Testimonial.objects.filter(status=True),
        'partners': Partner.objects.all().order_by("rank"),
    })
    
    return render(request, template, context)

#------------------------SUBSCRIPTION---------------------------------------


#------------------------SUBSCRIBE---------------------------------------SUBSCRIBE
def subscription(request):
    template_name = 'services/subscribe.html'
    initial_email = request.GET.get('email', '')
    
    captcha_form = CaptchaForm()
    context = {
        "initial_email": initial_email,
        "captcha_form": captcha_form,
    }
    if request.POST.get('form-type') == "subscribe":
                newsletter_email = request.POST.get('subscriber')
                if newsletter_email:
                    try:
                        duplicate = Subscriber.objects.get(email=newsletter_email)
                        if duplicate:
                            messages.warning(request, _("This email already exists in our database!"))
                            return redirect('home')
                    except:
                        if captcha_form.is_valid():
                            #-----------------------SAVE IN DATABASE----------------
                            sub = Subscriber(email=newsletter_email, conf_num=random_digits(), timestamp=datetime.now())
                            sub.save()

                            #---------------------send confirmation email settings------
                            sub_subject = _("Newsletter Bucegi Natural Park")
                            from_email='contact@bucegipark.ro'
                            sub_message = ''
                            html_content=_("Thank you for subscribing to our newsletter! You can finalize the process by clicking on this <a style='padding:2px 1px;border:2px solid black;background-color:black;color:white;font-weight:500;text-decoration:none;' href='{}{}/subscription-confirmation/?email={}&conf_num={}'> button</a>.".format('https://www.bucegipark.ro/',request.LANGUAGE_CODE, sub.email, sub.conf_num))
                            try:
                                send_mail(sub_subject, sub_message, from_email, [sub], html_message=html_content)
                                messages.success(request, _("A confirmation link was sent to your email inbox. Please check!"))
                                return redirect('home')
                            except Exception as e:
                                messages.warning(request, e)
                                return redirect('home')
                        else:
                            messages.warning(request, _(f'Human verification failed.'))
    return render(request, template_name, context)
#------------------------CONTACT apge------------------------------------CONTACT
def contacts_view(request):
    template_name = 'services/contact.html'
    if request.method == "POST":
        message_form = ContactForm(request.POST or None)
        form = CaptchaForm(request.POST)
        try:
            if form.is_valid():
                if message_form.is_valid():
                    message_subject = message_form.cleaned_data.get('subject')
                    message_author = message_form.cleaned_data.get('author')
                    sender_email = message_form.cleaned_data.get('email')
                    message = message_form.cleaned_data.get('text')
                    #=======send email=======
                    new_message = message_form.save(commit=False)
                    new_message.timestamp = datetime.now()
                    new_message.save()
                    send_mail(message_subject, message, sender_email, ['bucegipark@gmail.com'], fail_silently=False)
                    messages.success(request, _(f'Thank you for writing us {message_author}! We will answer as soon as possible.'))
                    return redirect('/contact')
                    # except Exception as e:
                    #     messages.warning(request, f'Error: {e}!')
                    #     return render(request, 'services/invalid_header.html',{})
                    # return HttpResponseRedirect('/contact')
                else:
                    messages.warning(request, _("Failed! Please make sure your info is correct!"))
                    return redirect('/contact')
            else:
                messages.warning(request, _("Failed! Please fill in the captcha field again!"))
                return redirect('/contact')
        except Exception as e:
            messages.warning(request, f"{e}")
    else:
        message_form = ContactForm()
        form = CaptchaForm()
    return render(request, template_name, {'message_form':message_form, 'form': form})
#======================== coming soon view================================
def coming_soon(request):
    template = 'services/coming-soon.html'
    return render(request, template, {})
#======================== events view================================
def eventlist_view(request):
    template = 'services/events.html'

    context = {"events":Event.objects.all().order_by("-timestamp")}
    return render(request, template, context)
#======================== events detail page================================
class EventDetailView(DetailView):
    model = Event
    template_name = 'services/event-details.html'
    context_object_name = 'event'
    slug_field = 'slug'
    count_hit = True
#======================== gallery page================================
def sector_map_view(request):
    template = 'services/sector-map.html'
    # if request.method == "POST":
    #     gallery_form =  GalleryForm()
    #     if gallery_form.is_valid():
    #         new_photo = gallery_form.save()
    # else:
    #     gallery_form =  GalleryForm()
    context = {
        "rangers_bv": Team.objects.filter(job__exact="Ranger",judet__exact="Brașov").order_by("surname"),
        "rangers_db": Team.objects.filter(job__exact="Ranger",judet__exact="Dâmbovița").order_by("surname"),
        "rangers_ph": Team.objects.filter(job__exact="Ranger",judet__exact="Prahova").order_by("surname")

    }
    return render(request, template, context)
#======================== gallery page================================
def gallery(request):
    template = 'services/gallery.html'
    # if request.method == "POST":
    #     gallery_form =  GalleryForm()
    #     if gallery_form.is_valid():
    #         new_photo = gallery_form.save()
    # else:
    #     gallery_form =  GalleryForm()
    context = {
        "attr_categ": AttractionCategory.objects.all(),
        "pics": Attraction.objects.all(),

    }
    return render(request, template, context)
#====================== video view ==========================================
def video_view(request):
    template = 'services/videos.html'
    #---------------------fetch YOUTUBE cid IDs-----------------------
    # p_url = 'https://www.googleapis.com/youtube/v3/search'
    # s_url = 'https://www.googleapis.com/youtube/v3/channels'
    # p_params = {
    #     'part': 'snippet',
    #     'channelId': 'UCITVdHG3i6bYsv01X24lBkA',
    #     'type': 'video',
    #     'key': settings.YOUTUBE_DATA_API_KEY,
    # }
    # s_params = {
    #     'part': 'statistics',
    #     'id': 'UCITVdHG3i6bYsv01X24lBkA',
    #     'key': settings.YOUTUBE_DATA_API_KEY,
    # }
    # videos = []
    # s_count = 0
    # url_list = []
    # try:
    #     p_req = requests.get(p_url, params=p_params)
    #     s_req = requests.get(s_url, params=s_params)
    #     p_results = p_req.json()['items']
    #     s_count = s_req.json()['items'][0]['statistics']['subscriberCount']
    #     for p_result in p_results:
    #         video_data = {
    #             'id': p_result['id']['videoId'],
    #             'embed': f'http://www.youtube.com/embed/{ p_result["id"]["videoId"] }',
    #             'url': f'https://www.youtube.com/watch?v={ p_result["id"]["videoId"] }',
    #             'title': p_result['snippet']['title'],
    #             'date': p_result['snippet']['publishedAt'][:4],
    #             'thumbnail':p_result['snippet']['thumbnails']['high']['url'],
    #         }
    #
    #         videos.append(video_data)
    # except Exception as e:
    #     messages.error(request, _('Nereusit!'))
    return render(request, template, {})
#--------------------------------------------------------------subscription_conf
@csrf_protect
def subscription_conf_view(request):
    template = 'services/subscription_conf.html'

    try:
        sub = Subscriber.objects.get(email=request.GET['email'])
        if sub.conf_num == request.GET['conf_num']:
            try:
                sub.confirmed = True
                sub.save()
            except:
                messages.warning(request, _("Error! Your email cannot be registered. Please contact our IT department at +40 758 039 784"))
            return render(request, template, {'email': sub.email, 'action': 'confirmed'})
        else:
            return render(request, template, {'email': sub.email, 'action': 'denied'})
    except Exception as e:
        messages.warning(request, e)
        return render(request, template, {})

#---------------------------SUBS DELETION VIEW------------------------------
def unsubscribe(request):
    template = 'services/unsubscribe.html'
    if request.method == "POST":
        unsub_email = request.POST.get('unsub_email')
        if unsub_email:
            try:
                sub = Subscriber.objects.get(email=unsub_email)
                if sub:
                    sub.delete()
                    messages.success(request, _("Success! Unsubscribing was finalized. If you change your mind you can subscribe again anytime"))
                    return render(request, template, {'email': sub.email, 'action': 'unsubscribed'})
                else:
                    messages.warning(request, _("Error! Unsubscribing failed. This email does not exist in our database"))
                    return redirect('/')
            except:
                messages.warning(request, _("Error! Unsubscribing failed. Please contact our IT department at +40 758 039 784"))
                return render(request, template, {'action': 'denied'})
        else:
            messages.warning(request, _("Error! Email incorrect."))
            return render(request, template, {})
    else:
        return render(request, template, {})

#========================history page================================
def history(request):
    template = 'services/history.html'
    return render(request, template, {})
#========================team page================================
def team(request):
    template = 'services/team.html'

    context = {
        'dir_members': Team.objects.filter(hierarchy=0),
        'adm_members': Team.objects.filter(hierarchy=1).order_by("surname"),
        'field_members': Team.objects.filter(hierarchy=2).order_by("surname"),
    }
    return render(request, template, context)
#========================council page================================
def council_view(request):
    template = 'services/consiliul_stiintific.html'

    context = {
        'president': SCouncil.objects.filter(hierarchy=0),
        'other_members': SCouncil.objects.filter(hierarchy=1).order_by("surname"),
    }
    return render(request, template, context)
#========================wildlife page================================
def wildlife(request):
    template = 'services/wildlife.html'

    context = {
        'wildlife_categ': WildlifeCategory.objects.all(),
        'wildlife': Wildlife.objects.all(),
    }
    return render(request, template, context)

#======================== wildlife detail page================================
class WildlifeDetailView(DetailView):
    model = Wildlife
    template_name = 'services/wildlife-details.html'
    context_object_name = 'willdife'
    slug_field = 'slug'
    count_hit = True
#========================flora page================================
def flora(request):
    template = 'services/flora.html'

    context = {
        'flora_categ': FloraCategory.objects.all(),
        'flora': Flora.objects.all(),
    }
    return render(request, template, context)
#======================== flora detail page================================
class FloraDetailView(DetailView):
    model = Flora
    template_name = 'services/flora-details.html'
    context_object_name = 'flora'
    slug_field = 'slug'
    count_hit = True
#========================INFO VIEW================================
def ticket_info(request):
    template = 'services/ticket-info.html'
    return render(request, template, {})
#========================THEME TRAILS page================================
def theme_trails(request):
    template = 'services/theme-trails.html'

    return render(request, template, {})
#========================mass-media page================================
def massmedia(request):
    template = 'services/mass-media.html'
    return render(request, template, {})

#======================== public documents page================================
def public_docs(request):
    template = 'public_docs/public_docs.html'

    context = {
    'public_docs': PublicCategory.objects.all(),
    'links':PublicCatLink.objects.all()
    }
    return render(request, template, context)
#======================== consulting council documents pages================================

#========================mng plan documents view =================
def mng_plan_view(request):
    template_name = 'public_docs/mng-plan.html'
    context ={}
    context.update(
        {'mngplan_docs': MngPlanDocsCategory.objects.all(),
         'mngplan_links': MngPlanCatLink.objects.all(),
        }
    )
    return render(request, template_name, context)
#========================park regulations view =================
def park_regulation_view(request):
    template_name = 'public_docs/park-regulation.html'
    context ={}
    context.update(
        {'park_regulation': ParkRegulationCategory.objects.all(),
         'park_reg_links': ParkRegulationCatLink.objects.all(),
        }
    )
    return render(request, template_name, context)
#======================== faq page================================
def faq_view(request):
    template = 'services/faq.html'

    context = {
    }
    return render(request, template, context)
#======================== privacy page================================
def privacy_view(request):
    template = 'services/privacy.html'
    return render(request, template, {})
#======================== terms page================================
def terms_view(request):
    template = 'services/terms.html'
    return render(request, template, {})
#======================== info points page================================
def infopoints_view(request):
    template = 'services/info-points.html'
    context = {}
    return render(request, template, context)
#======================== announcement main page================================
class AnnouncementView(ListView):
    model = Announcement
    template_name = 'services/announcements.html'
    context_object_name = 'announcements'
    ordering = ['-timestamp']
    paginate_by = 3
    def get_context_data(self, **kwargs):          
        context = super().get_context_data(**kwargs)                     
        context["group_archive"] = Announcement.objects.order_by('timestamp')
        return context
# def announcement_view(request):
#     template = 'services/announcements.html'
#     announc = Announcement.objects.all().order_by('-timestamp'),
#     pag = Paginator(announc, 3)  # creating a paginator object
#     page_number = request.GET.get('page')
#     try:
#         page_obj = pag.page(page_number)  # returns the desired page object
#     except PageNotAnInteger:
#         # if page_number is not an integer then assign the first page
#         page_obj = pag.page(1)
#     except EmptyPage:
#         # if page is empty then return last page
#         page_obj = pag.page(pag.num_pages)

#     context = {
#     "page_obj":page_obj,
#     "group_archive": Announcement.objects.order_by('timestamp'),
#     }

#     return render(request, template, context)
#======================== announcement archive page================================
# class ArticleMonthArchiveView(MonthArchiveView):
#     queryset = Announcement.objects.all()
#     date_field = "timestamp"
#     allow_future = True
#     def get_month(self):
#         try:
#             month = super(ArticleMonthArchiveView, self).get_month()
#         except Http404:
#             month = now().strftime(self.get_month_format())

#         return month

#     def get_year(self):
#         try:
#             year = super(ArticleMonthArchiveView, self).get_year()
#         except Http404:
#             year = now().strftime(self.get_year_format())

#         return year
#======================== announcement detail page================================
class AnnounDetailView(HitCountDetailView):
    model = Announcement
    template_name = 'services/announc-details.html'
    context_object_name = 'announcement'
    slug_field = 'slug'
    # set to True to count the hit
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(AnnounDetailView, self).get_context_data(**kwargs)
        return context

        return super().form_valid(form)
    def announcement(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)
#======================== blog main page================================
# def bloglist_view(request):
#     template = 'blog/blog.html'
#     posts_categs = {}
#     if request.method=="POST":
#         newsletter_email = request.POST.get('subscriber')
#         #--------------check if newsletter email exists already---------
#         if "subscriber" in request.POST:
#             if newsletter_email:
#                 try:
#                     duplicate = Subscriber.objects.get(email=newsletter_email)
#                     if duplicate:
#                         messages.warning(request, _("This email already exists in our database!"))
#                         return redirect('blog')
#                 except:
#                     #-----------------------SAVE IN DATABASE----------------
#                     sub = Subscriber(email=newsletter_email, conf_num=random_digits(), timestamp=datetime.now())
#                     sub.save()

#                     #---------------------send confirmation email settings------
#                     sub_subject = _("Newsletter Bucegi Natural Park")
#                     from_email='contact@bucegipark.ro'
#                     sub_message = ''
#                     html_content=_("Thank you for subscribing to our newsletter! You can finalize the process by clicking on this <a style='padding:2px 1px;border:2px solid black;background-color:black;color:white;font-weight:500;text-decoration:none;' href='{}{}/subscription-confirmation/?email={}&conf_num={}'> button</a>.".format('https://www.bucegipark.ro/',request.LANGUAGE_CODE, sub.email, sub.conf_num))
#                     try:
#                         send_mail(sub_subject, sub_message, from_email, [sub], html_message=html_content)
#                         messages.success(request, _("A confirmation link was sent to your email inbox. Please check!"))
#                         return redirect('blog')
#                     except Exception as e:
#                         messages.warning(request, e)
#                         return redirect('blog')


#     context = {
#     "blogposts": BlogPost.objects.all().order_by("-created_date"),
#     "categories": BlogPostCategory.objects.all(),
#     # "group_archive": group_archive,
#     # "group_categ":group_categ,
#     }

#     return render(request, template, context)

#======================== blog detail page================================
# class PostDetailView(HitCountDetailView, FormMixin):
#     model = BlogPost
#     template_name = 'blog/blog-details.html'
#     context_object_name = 'blogpost'
#     slug_field = 'slug'
#     form_class = CommentForm
#     # set to True to count the hit
#     count_hit = True

#     def get_context_data(self, **kwargs):
#         context = super(PostDetailView, self).get_context_data(**kwargs)
#         posts = BlogPost.objects.all()
#         form = self.get_form()
#         comms = Comment.objects.filter(post=BlogPost.objects.get(slug=self.object.slug))
#         context.update({
#         # ----------- most viewed posts---------------------------------------
#         # 'popular_posts': posts.order_by('-hit_count_generic__hits')[:3],
#         # ----------- comments -------------------------------------------
#         'comms': comms,
#         'comments': comms.count(),
#         # ----------- recent posts ---------------------------------------
#         'recent_posts': posts.order_by("-created_date")[:5],
#         # ----------- most posts  ---------------------------------------
#         'posts': posts,
#         'form': form,
#         'form_captcha': CaptchaForm()
#         })
#         return context
#     def form_valid(self, form):
#         # This method is called when valid form data has been POSTed.
#         # It should return an HttpResponse.
#         form.save()
#         return super().form_valid(form)
#     def post(self, request, *args, **kwargs):
#         return self.get(request, *args, **kwargs)
#======================== blog search page================================
# def blogsearch_view(request):
#     template = 'blog/blog_search.html'
#     context = {}
#     blog_posts = BlogPost.objects.all()
#     if request.method == "GET":
#         query = request.GET.get("search")
#         queryset = blog_posts.filter(Q(title__icontains=query) | Q(text__icontains=query))
#         if queryset:
#             count = queryset.count()
#             context.update({
#                 "count":count,
#                 "query":query,
#                 "posts":queryset,

#             })
#         else:
#             messages.warning(request, _("We did not find any posts containing that word!"))

#         return render(request, template, context)
#=========================parc rules view======================================
def park_rules(request):
    template = 'services/rules.html'
    context = {}
    return render(request, template, context)
#=========================videos view ==========================================
def videos_view(request):
    template_name = 'services/videos.html'
    #---------------------fetch vid IDs-----------------------
    p_url = 'https://www.googleapis.com/youtube/v3/search'
    p_params = {
        'part': 'snippet',
        'channelId': settings.CHANNELID,
        'type': 'video',
        'key': settings.YOUTUBE_DATA_API_KEY,
    }
    videos = []
    try:
        p_req = requests.get(p_url, params=p_params)
        p_results = p_req.json()['items']
        for p_result in p_results:
            video_data = {
                'id': p_result['id']['videoId'],
                'embed': f'http://www.youtube.com/embed/{ p_result["id"]["videoId"] }',
                'url': f'https://www.youtube.com/watch?v={ p_result["id"]["videoId"] }',
                'title': p_result['snippet']['title'],
                'date': p_result['snippet']['publishedAt'][:4],
                'thumbnail':p_result['snippet']['thumbnails']['high']['url'],
            }

            videos.append(video_data)
    except Exception as e:
        messages.error(request, _('Import video nereusit!'))
    context = {
        "videos": videos,
    }
    return render(request, template_name, context)