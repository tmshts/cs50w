from asyncio.windows_events import NULL
from logging import PlaceHolder
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bid, Watchlist

from django.contrib.auth.decorators import login_required
from django import forms


class ListingForm(forms.Form):
    title = forms.CharField(label="",
                            max_length=200,
                            widget= forms.TextInput
                            (attrs={'placeholder': 'Write Title Of Your Listing'}))
    description = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'Write Description'}))
    price = forms.FloatField()
    image_url = forms.URLField(max_length=2000, required=False)


class WatchlistForm(forms.Form):
    listing_id = forms.CharField(widget=forms.HiddenInput())

class BidForm(forms.Form):
    bid = forms.FloatField(label="", required=False)

class WatchForm(forms.Form):
    delete_id = forms.CharField(widget=forms.HiddenInput())

class NotActiveForm(forms.Form):
    not_active = forms.CharField(required=False, widget=forms.HiddenInput())
    #not_active = forms.BooleanField(label="", required=False)

class CommentForm(forms.Form):
    content_of_comment = forms.CharField(required=False, label="", widget=forms.Textarea(attrs={'placeholder': 'Write Your Comment'}))


# I am aware of my bad design/style of code. There are too much redundancy, especially in the return render request - context. I would be happy to get some feedback which can help me to modify it or to get better for next assignment.

def categories(request):
    if request.method == "POST":

            value_category = request.POST.get('category', False)
            if value_category:
                category_instance = Category.objects.get(pk=int(value_category))
                listings = Listing.objects.filter(category_of_listing=category_instance).exclude(not_active=True).values().order_by('id').reverse()
                name_category = category_instance.name_of_category

                # redundancy again !
                current_prices = []
                listings_id = listings.values_list('pk', flat=True)

                for number in listings_id:
                    max_object = maxbid(number)
                    if isinstance(max_object, float):
                        current_prices.append(max_object)
                    else:
                        maximal = max_object.price_of_bid
                        current_prices.append(maximal)

                zipped_list = zip(listings, current_prices)

                return render(request, "auctions/categories.html", {
                    "context": zipped_list,
                    "categories": Category.objects.all(),
                    "name_category": name_category
                })              

            else:          
                return HttpResponseRedirect(reverse("categories",))


    else: #GET
        #listings = Listing.objects.all().order_by('id').reverse()
        
        return render(request, "auctions/categories.html", {
            #"listings": listings, # Alternative to list all the active listings anyways
            "categories": Category.objects.all(),
        })

def closedlistings(request):
    listings = Listing.objects.exclude(not_active=False).order_by('id').reverse()
    current_prices = []
    listings_id = listings.values_list('pk', flat=True)

    for number in listings_id:
        max_object = maxbid(number)
        if isinstance(max_object, float):
            current_prices.append(max_object)
        else:
            maximal = max_object.price_of_bid
            current_prices.append(maximal)

    zipped_list = zip(listings, current_prices)

    return render(request, "auctions/closedlistings.html", {
        "context": zipped_list
    })

def index(request):
    listings = Listing.objects.exclude(not_active=True).order_by('id').reverse()
    current_prices = []
    listings_id = listings.values_list('pk', flat=True)

    for number in listings_id:
        max_object = maxbid(number)
        if isinstance(max_object, float):
            current_prices.append(max_object)
        else:
            maximal = max_object.price_of_bid
            current_prices.append(maximal)

    zipped_list = zip(listings, current_prices)

    return render(request, "auctions/index.html", {
        "context": zipped_list
    })


def maxbid(listing_id):
        listings = Listing.objects.get(pk=listing_id)
        get_bids = listings.listing_bid.all()
        if not get_bids:
            return listings.starting_bid_of_listing # float
        else:
            max_bid = get_bids.order_by('-price_of_bid')[0] # object
            return max_bid

@login_required
def watchlist(request):

    watchlistform = WatchlistForm(request.POST)
    bidform = BidForm(request.POST)
    not_active_form = NotActiveForm(request.POST)
    comment_form = CommentForm(request.POST)   

    if request.method == "POST":

        if 'listing_id' in request.POST: # in listings.html
            if watchlistform.is_valid():
                listing = watchlistform.cleaned_data['listing_id']
                listing_instance = Listing.objects.get(pk=listing)
                username_instance = User.objects.get(pk=request.user.id)
                if Watchlist.objects.filter(watchlist_for_listing=listing, watchlist_from_user=username_instance).values():
                    listings = Listing.objects.get(pk=listing)
                    get_bids = listings.listing_bid.all()
                    count_bid = get_bids.count()
                    messagedatabase = "Already in your Watchlist."
                    get_comments = listings.listing_comment.all()
                    if listings.listed_by_user == request.user:
                        # user can closed listing even if there are no bids - he might have changed mind
                        if len(get_bids) == 0:
                            return render(request, "auctions/listings.html", {
                            "listings": listings,
                            "number": count_bid,
                            "bidform": bidform,
                            "watchlistform": watchlistform,
                            "messagedatabase": messagedatabase,
                            "not_active_form": not_active_form,
                            "comment_form": comment_form,
                            "get_comments": get_comments
                            })
                        else:
                            return render(request, "auctions/listings.html", {
                                "listings": listings,
                                "bids": maxbid(listing), ##################
                                "number": count_bid,
                                "bidform": bidform,
                                "watchlistform": watchlistform,
                                "messagedatabase": messagedatabase,
                                "not_active_form": not_active_form,
                                "comment_form": comment_form,
                                "get_comments": get_comments
                            })
                    else:
                        if len(get_bids) == 0:
                            return render(request, "auctions/listings.html", {
                            "listings": listings,
                            "number": count_bid,
                            "bidform": bidform,
                            "watchlistform": watchlistform,
                            "messagedatabase": messagedatabase,
                            "comment_form": comment_form,
                            "get_comments": get_comments
                            })
                        else:
                            return render(request, "auctions/listings.html", {
                                "listings": listings,
                                "bids": maxbid(listing), ##################
                                "number": count_bid,
                                "bidform": bidform,
                                "watchlistform": watchlistform,
                                "messagedatabase": messagedatabase,
                                "comment_form": comment_form,
                                "get_comments": get_comments
                            })


                else:
                    Watchlist.objects.create(watchlist_for_listing=listing_instance, watchlist_from_user=username_instance)
                    return HttpResponseRedirect(reverse("watchlist",))

        else:  #'delete_id' in request.POST: # in watchlist.html
            watchform = WatchForm(request.POST)
            if watchform.is_valid():
                listing = watchform.cleaned_data['delete_id']
                item = Watchlist.objects.get(watchlist_for_listing=listing, watchlist_from_user=request.user.id)
                item.delete()
                return HttpResponseRedirect(reverse("watchlist",))            


    else: # GET
        watchlist_queryset = Watchlist.objects.filter(watchlist_from_user=request.user.id).values().order_by('id').reverse()
        #pokus = Watchlist.objects.filter(watchlist_from_user=request.user.id).values()

        watch_list = []
        for watchlist in watchlist_queryset:
            watch_list.append(watchlist['watchlist_for_listing_id']) #watchlist_for_listing_id in queryset

        listings = Listing.objects.filter(id__in=watch_list)


        current_prices = []
        listings_id = listings.values_list('pk', flat=True)

        for number in listings_id:
            max_object = maxbid(number)
            if isinstance(max_object, float):
                current_prices.append(max_object)
            else:
                maximal = max_object.price_of_bid
                current_prices.append(maximal)

        zipped_list = zip(listings, current_prices)

        return render(request, "auctions/watchlist.html", {
            "context": zipped_list
        })

def listings(request, listing_id):
    bidform = BidForm(request.POST)
    comment_form = CommentForm(request.POST)
    not_active_form = NotActiveForm(request.POST)


    if request.method == "POST":

        if 'bid_submit' in request.POST:
            if bidform.is_valid():
                bid = bidform.cleaned_data['bid']
                listing_instance = Listing.objects.get(pk=int(listing_id))
                starting_price = listing_instance.starting_bid_of_listing
                username_instance = User.objects.get(pk=request.user.id)
                listings = Listing.objects.get(pk=listing_id)
                get_comments = listings.listing_comment.all()
                get_bids = listings.listing_bid.all()
                count_bid = get_bids.count()
                if len(get_bids) == 0:
                    if bid is None:
                        bid_message = "You must place a bid."
                        listings = Listing.objects.get(pk=listing_id)
                        return render(request, "auctions/listings.html", {
                            "listings": listings,
                            "number": count_bid,
                            "bidform": bidform,
                            "bid_message": bid_message,
                            "get_comments": get_comments,
                            "comment_form": comment_form
                            })

                    elif bid >= starting_price:
                        Bid.objects.create(price_of_bid=bid, bid_for_listing=listing_instance, bid_from_user=username_instance)
                        listings = Listing.objects.get(pk=listing_id)
                        get_bids = listings.listing_bid.all()
                        count_bid = get_bids.count()
                        return render(request, "auctions/listings.html", {
                            "listings": listings,
                            "number": count_bid,
                            "bidform": bidform,
                            "bids": maxbid(listing_id), ##########
                            "get_comments": get_comments,
                            "comment_form": comment_form
                            })

                    else:
                        bid_message = "The bid must be at least as large as the starting bid"
                        return render(request, "auctions/listings.html", {
                            "listings": listings,
                            "number": count_bid,
                            "bidform": bidform,
                            "bid_message": bid_message,
                            "get_comments": get_comments,
                            "comment_form": comment_form
                            })


                else: # len(get_bids) > 0
                    if bid is None:
                        bid_message = "You must place a bid."
                        listings = Listing.objects.get(pk=listing_id)
                        return render(request, "auctions/listings.html", {
                            "listings": listings,
                            "number": count_bid,
                            "bidform": bidform,
                            "bid_message": bid_message,
                            "bids": maxbid(listing_id), ##########
                            "get_comments": get_comments,
                            "comment_form": comment_form
                            })
                    elif bid >= starting_price and bid > maxbid(listing_id).price_of_bid:
                        Bid.objects.create(price_of_bid=bid, bid_for_listing=listing_instance, bid_from_user=username_instance)
                        listings = Listing.objects.get(pk=listing_id)
                        get_bids = listings.listing_bid.all()
                        count_bid = get_bids.count()
                        return render(request, "auctions/listings.html", {
                            "listings": listings,
                            "number": count_bid,
                            "bidform": bidform,
                            "bids": maxbid(listing_id), ##########
                            "get_comments": get_comments,
                            "comment_form": comment_form
                        })
                    else:
                        bid_message = "The bid must be at least as large as the starting bid and must be greater than max bid."
                        listings = Listing.objects.get(pk=listing_id)
                        return render(request, "auctions/listings.html", {
                            "listings": listings,
                            "number": count_bid,
                            "bidform": bidform,
                            "bid_message": bid_message,
                            "bids": maxbid(listing_id), ##########
                            "get_comments": get_comments,
                            "comment_form": comment_form
                            })

        elif 'comment_id' in request.POST: # in listings.html
            if comment_form.is_valid():
                comment = comment_form.cleaned_data['content_of_comment']
                listing_instance = Listing.objects.get(pk=int(listing_id))
                username_instance = User.objects.get(pk=request.user.id)
                Comment.objects.create(content_of_comment=comment, comment_in_listing=listing_instance, comment_from_user=username_instance)
                return HttpResponseRedirect(reverse("listings", args=(listing_id,)))
            


        elif 'not_active' in request.POST: # in listings.html
            not_active_form = NotActiveForm(request.POST)
            if not_active_form.is_valid():
                #new_listing_id = NotActiveForm.cleaned_data['not_active']
                listings = Listing.objects.get(pk=listing_id)
                listings.not_active = True
                listings.save()
                get_bids = listings.listing_bid.all()
                count_bid = get_bids.count()
                return HttpResponseRedirect(reverse("listings", args=(listing_id,)))


        else: #'listing_submit' in request.POST: # in categories.html, closedlistings.html and index.html
            listings = Listing.objects.get(pk=listing_id)
            get_comments = listings.listing_comment.all()
            get_bids = listings.listing_bid.all()
            count_bid = get_bids.count()
            if listings.not_active == True:
                return HttpResponseRedirect(reverse("listings", args=(listing_id,)))
            else:
                if listings.listed_by_user == request.user:
                    # user can closed listing even if there are no bids - he might have changed mind
                    if len(get_bids) == 0:
                        return render(request, "auctions/listings.html", {
                            "listings": listings,
                            "number": count_bid,
                            "bidform": bidform,
                            "not_active_form": not_active_form,
                            "get_comments": get_comments,
                            "comment_form": comment_form
                            })
                    else:
                        return render(request, "auctions/listings.html", {
                            "listings": listings,
                            "number": count_bid,
                            "bidform": bidform,
                            "bids": maxbid(listing_id), ####################
                            "not_active_form": not_active_form,
                            "get_comments": get_comments,
                            "comment_form": comment_form
                        })
                else:
                    if len(get_bids) == 0:
                        return render(request, "auctions/listings.html", {
                            "listings": listings,
                            "number": count_bid,
                            "bidform": bidform,
                            "get_comments": get_comments,
                            "comment_form": comment_form
                            })
                    else:
                        return render(request, "auctions/listings.html", {
                            "listings": listings,
                            "number": count_bid,
                            "bidform": bidform,
                            "bids": maxbid(listing_id), ####################
                            "get_comments": get_comments,
                            "comment_form": comment_form
                        })

    else: #GET
        #not_active_form = NotActiveForm(request.POST)
        listings = Listing.objects.get(pk=listing_id)
        get_bids = listings.listing_bid.all()
        count_bid = get_bids.count()
        get_comments = listings.listing_comment.all()
        not_active_message = "The listing is closed"
        if listings.not_active == True:
            maxi_bid = maxbid(listing_id)
            if isinstance(maxi_bid, float): # just starting price
                winning_message = "There was no highest bid -> no winner."
                return render(request, "auctions/nolistings.html", {
                        "listings": listings,
                        "number": count_bid,
                        "not_active_message": not_active_message,
                        "winning_message": winning_message,
                        "get_comments": get_comments
                        })
            else: # at least 1 person bid
                maxi_bid_from_user = maxi_bid.bid_from_user
                winning_message = "Congratulations ! You won this listing."
                if maxi_bid_from_user == request.user:
                    return render(request, "auctions/nolistings.html", {
                        "listings": listings,
                        "number": count_bid,
                        "not_active_message": not_active_message,
                        "winning_message": winning_message,
                        "bids": maxbid(listing_id), ##############################
                        "get_comments": get_comments
                        })

                else: # just regular user who did not win
                    return render(request, "auctions/nolistings.html", {
                        "listings": listings,
                        "number": count_bid,
                        "bids": maxbid(listing_id), ##############################
                        "not_active_message": not_active_message,
                        "get_comments": get_comments
                    })


        else:
            #not_active_form = NotActiveForm(request.POST)
            listings = Listing.objects.get(pk=listing_id)
            get_bids = listings.listing_bid.all()
            count_bid = get_bids.count()

            if listings.listed_by_user == request.user:
                if len(get_bids) == 0:
                    return render(request, "auctions/listings.html", {
                    "listings": listings,
                    "number": count_bid,
                    "bidform": bidform,
                    "not_active_form": not_active_form,
                    "comment_form": comment_form,
                    "get_comments": get_comments
                })
                else:
                    return render(request, "auctions/listings.html", {
                    "listings": listings,
                    "number": count_bid,
                    "bidform": bidform,
                    "bids": maxbid(listing_id), ##############################
                    "not_active_form": not_active_form,
                    #"watchlistform": watchlistform
                    "comment_form": comment_form,
                    "get_comments": get_comments
                })
            else:
                if len(get_bids) == 0:
                    return render(request, "auctions/listings.html", {
                    "listings": listings,
                    "number": count_bid,
                    "bidform": bidform,
                    "comment_form": comment_form,
                    "get_comments": get_comments
                })
                else:
                    return render(request, "auctions/listings.html", {
                    "listings": listings,
                    "number": count_bid,
                    "bidform": bidform,
                    "bids": maxbid(listing_id), ##############################
                    #"watchlistform": watchlistform
                    "comment_form": comment_form,
                    "get_comments": get_comments
                })

@login_required
def create(request):
    if request.method == "POST":
        # request.POST["category"] refers to <select name="category">
        # I get PK of one category and this object is saved in variable category
        form = ListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            # Alternative
            #title = request.POST.get('title')
            description = form.cleaned_data["description"]
            # I get Category object (9)
            price = form.cleaned_data["price"]
            url_image = form.cleaned_data["image_url"]
            # I get username tmshts
            username_instance = User.objects.get(pk=request.user.id)
            username_id = request.user.id

            value_category = request.POST.get('category', False)
            if value_category:
                category_instance = Category.objects.get(pk=int(value_category))
            
                Listing.objects.create(title_of_listing=title, description_of_listing=description, image_of_listing=url_image, starting_bid_of_listing = price, category_of_listing=category_instance, listed_by_user=username_instance)

                return HttpResponseRedirect(reverse("index"))

            else:          
                Listing.objects.create(title_of_listing=title, description_of_listing=description, image_of_listing=url_image, starting_bid_of_listing = price, category_of_listing=None, listed_by_user=username_instance)

                return HttpResponseRedirect(reverse("index"))
            
    else: # GET
        form = ListingForm()
        return render(request, "auctions/create_listing.html", {
            "categories": Category.objects.all(),
            'form': form
        })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
