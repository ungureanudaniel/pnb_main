from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from utils.weather_scrape import scraped_data
from django.views.decorators.gzip import gzip_page
import datetime
from django.contrib import messages
import random
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
import requests
from django.utils.translation import gettext_lazy as _
#----blog imports
from django.db.models import Q
from django.db.models import Count
from django.views.generic.edit import FormMixin
from hitcount.views import HitCountDetailView

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

    if request.method=='POST':
        review_form = TestimonialForm(request.POST or None, request.FILES or None)
        try:
            if review_form.is_valid():
                new_review = review_form.save(commit=False)
                new_review.status = False
                new_review.save()
            else:
                messages.error(request, "Please check for empty fields.")
                return redirect('.')
        except Exception as e:
            messages.error(request, "Please check for empty fields.")

    return render(request, template, {"review_form":TestimonialForm()})

#========================add attraction view=================================
# def add_attraction(request):
#     template = 'services/add_attraction.html'
#
#     if request.method=='POST':
#         attr_form = AttractionForm()
#         try:
#             if review_form.is_valid():
#                 new_review = review_form.save(commit=False)
#                 new_review.status = False
#                 new_review.save()
#             else:
#                 messages.error(request, "Please check for empty fields.")
#                 return redirect('.')
#         except Exception as e:
#             messages.error(request, "Please check for empty fields.")
#
#     return render(request, template, {"attr_form":AttractionForm()})
#========================home page=================================
@gzip_page
def home(request):
    template = 'services/home.html'
    weather = scraped_data()
    context = {
        "weather": weather,
        "captcha_form": CaptchaForm()
    }
    if request.method=='POST':
        if request.POST.get('form-type') == "signin-form":
            captcha_form = CaptchaForm(request.POST or None)
            #---------user login functions-----------
            user = None
            try:
                username = request.POST.get('signin-name')
                password = request.POST.get('signin-password')
                # user_check = User.object.get(username = username)
                user = authenticate(username=username, password=password)
                if captcha_form.is_valid():
                    if user is not None:

                        try:
                            login(request, user)
                            context['user'] = username
                            return redirect('.')
                        except Exception as e:
                            messages.warning(request, _("Warning! {e}"))
                            return redirect('.')
                    else:
                        messages.warning(request, _("User does not exist!"))
                        return redirect('.')

                else:
                    messages.warning(request, _("Captcha incorrect!"))
                    return redirect('.')
            except (Exception, User.DoesNotExist) as e:
                messages.warning(request, _("Warning! {e}"))

        #--------------check if newsletter email exists already---------
        if request.POST.get('submit') == "subscribe":
            newsletter_email = request.POST.get('subscriber')
            if newsletter_email:
                try:
                    duplicate = Subscriber.objects.get(email=newsletter_email)
                    if duplicate:
                        messages.warning(request, _("This email already exists in our database!"))
                        return redirect('/')
                except:
                    #-----------------------SAVE IN DATABASE----------------
                    sub = Subscriber(email=newsletter_email, conf_num=random_digits(), timestamp=datetime.datetime.now())
                    sub.save()

                    #---------------------send confirmation email settings------
                    sub_subject = _("Newsletter Bucegi Natural Park")
                    from_email='contact@bucegipark.ro'
                    sub_message = ''
                    html_content=_('Thank you for subscribing to our newsletter!\
                                You can finalize the process by clicking on this \
                                    <a href="{}subscription_confirmation/?email={}&conf_num={}"> button \
                                        </a>.'.format('127.0.0.1:8000/', sub.email, sub.conf_num))
                    try:
                        send_mail(sub_subject, sub_message, from_email, [sub], html_message=html_content)
                        messages.success(request, _("A confirmation link was sent to your email inbox. Please check!"))
                        return redirect('/')
                    except BadHeaderError as e:
                        messages.warning(request, e)
                        return redirect('/')


    attr_c = AttractionCategory.objects.all()
    #fetching data from the database and adding to context dict
    context.update({
        'attr_categ': AttractionCategory.objects.all(),
        'attr': Attraction.objects.all(),
        'current_date': datetime.date.today(),
        'reviews': Testimonial.objects.filter(status=True),
        })
    return render(request, template, context)

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
                    print(f"{message_subject},{message_author},{sender_email}")
                    new_message = message_form.save(commit=False)
                    new_message.timestamp = datetime.datetime.now()
                    new_message.save()
                    send_mail(message_subject, message, sender_email, ['contact@bucegipark.ro'], fail_silently=False)
                    messages.success(request, _(f'Thank you for writting us {message_author}! We will answer as soon as possible.'))
                    return redirect('/contact')
                    # except Exception as e:
                    #     messages.warning(request, f'Error: {e}!')
                    #     return render(request, 'services/invalid_header.html',{})
                    # return HttpResponseRedirect('/contact')
                else:
                    messages.warning(request, "Failed! Please make sure your info is correct!")
                    return redirect('/contact')
            else:
                messages.warning(request, "Failed! Please fill in the captcha field again!")
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

    context = {"events":Event.objects.all()}
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
        "photos":Gallery.objects.all().order_by("name"),
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
        'field_members': Team.objects.filter(job__exact="Ranger").order_by("surname"),
    }
    return render(request, template, context)
#========================wildlife page================================
def wildlife(request):
    template = 'services/wildlife.html'

    context = {
        'attr': Attraction.objects.filter(categ='3'),
    }
    return render(request, template, context)
#========================flora page================================
def flora(request):
    template = 'services/flora.html'

    context = {
        'attr': Attraction.objects.filter(categ='4'),
    }
    return render(request, template, context)
#========================TICKETS INFO VIEW================================
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
    template = 'services/public_docs.html'

    context = {
    'public_docs': PublicCategory.objects.all(),
    }
    return render(request, template, context)
#======================== faq page================================
def faq_view(request):
    template = 'services/faq.html'

    context = {
    }
    return render(request, template, context)
#======================== page not found page================================
def page_not_found(request):
    template = 'services/404.html'
    return render(request, template, {})
#======================== invalid header page================================
def invalid_header(request):
    template = 'services/invalid_header.html'
    return render(request, template, {})
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
#======================== blog main page================================
def bloglist_view(request):
    template = 'blog/blog.html'
    posts_categs = {}
    #------- post per categories count using annotate---------
    group_categ = BlogPostCategory.objects.all().annotate(count=Count('postcategory')).values()
    group_archive = BlogPost.objects.values('created_date').annotate(count=Count('id')).values('created_date', 'count').order_by('created_date')
    if request.method=="POST":
        newsletter_email = request.POST.get('subscriber')
        #--------------check if newsletter email exists already---------
        if "subscriber" in request.POST:
            if newsletter_email:
                try:
                    duplicate = Subscriber.objects.get(email=newsletter_email)
                    if duplicate:
                        messages.warning(request, _("This email already exists in our database!"))
                        return redirect('blog')
                except:
                    #-----------------------SAVE IN DATABASE----------------
                    sub = Subscriber(email=newsletter_email, conf_num=random_digits(), timestamp=datetime.datetime.now())
                    sub.save()

                    #---------------------send confirmation email settings------
                    sub_subject = _("Newsletter Bucegi Natural Park")
                    from_email='contact@bucegipark.ro'
                    sub_message = ''
                    html_content=_('Thank you for subscribing to our newsletter!\
                                You can finalize the process by clicking on this \
                                    <a href="{}subscription_confirmation/?email={}&conf_num={}"> button \
                                        </a>.'.format('127.0.0.1:8000/', sub.email, sub.conf_num))
                    try:
                        send_mail(sub_subject, sub_message, from_email, [sub], html_message=html_content)
                        messages.success(request, _("A confirmation link was sent to your email inbox. Please check!"))

                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')

                    return render(request, template, {})

    context = {
    "blogposts": BlogPost.objects.all(),
    "categories": BlogPostCategory.objects.all(),
    "group_archive": group_archive,
    "group_categ":group_categ,
    }

    return render(request, template, context)
#======================== blog detail page================================
class PostDetailView(HitCountDetailView, FormMixin):
    model = BlogPost
    template_name = 'blog/blog-details.html'
    context_object_name = 'blogpost'
    slug_field = 'slug'
    form_class = CommentForm
    # set to True to count the hit
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        posts = BlogPost.objects.all()
        form = self.get_form()
        comms = Comment.objects.filter(post=BlogPost.objects.get(slug=self.object.slug))
        context.update({
        # ----------- most viewed posts---------------------------------------
        # 'popular_posts': posts.order_by('-hit_count_generic__hits')[:3],
        # ----------- comments -------------------------------------------
        'comms': comms,
        'comments': comms.count(),
        # ----------- recent posts ---------------------------------------
        'recent_posts': posts.order_by("-created_date")[:5],
        # ----------- most posts  ---------------------------------------
        'posts': posts,
        'form': form,
        'form_captcha': CaptchaForm()
        })
        return context
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.save()
        return super().form_valid(form)
    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)
#======================== blog search page================================
def blogsearch_view(request):
    template = 'blog/blog_search.html'
    context = {}
    blog_posts = BlogPost.objects.all()
    if request.method == "GET":
        query = request.GET.get("search")
        queryset = blog_posts.filter(Q(title__icontains=query) | Q(text__icontains=query))
        if queryset:
            count = queryset.count()
            context.update({
                "count":count,
                "query":query,
                "posts":queryset,

            })
        else:
            messages.warning(request, _("We did not find any posts containing that word!"))

        return render(request, template, context)
