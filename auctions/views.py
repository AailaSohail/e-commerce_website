from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib import messages
from django.urls import reverse
from .models import User,Category,Listing,Bids,Comments


def index(request):
    if request.method=="GET":
        Active_listing=Listing.objects.filter(active=True)
        return render(request, "auctions/index.html",{
        "active":Active_listing,
        "title":"Active Listing"
        })
    else:
        select_cat = request.POST['category']
        cat = Category.objects.get(category = select_cat)
        Active_listing=Listing.objects.filter(active=True, category = cat)
        return render(request, "auctions/index.html",{
        "active":Active_listing,
        "title":"Active Listing"
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

@login_required
def add_listing(request):
    categories = Category.objects.all()
    if request.method=="GET":
        return render(request, "auctions/add_list.html",{
        "categories": categories
        })
    else:
        user = request.user
        title =  request.POST['title']
        description =  request.POST['description']
        img_url =  request.POST['imageurl']
        price =  request.POST['price']
        category = request.POST['category']
        cat = Category.objects.get(category=category)
        if title=="" or description =="" or img_url == "" or price =="":
            return render(request, "auctions/add_list.html", {
            "message": "Fill ALL the empty forms",
            "categories": categories
            }) 
        else:  
            Listing.objects.create(owner=user,price=float(price),title=title,description=description,image=img_url,category=cat)
            return HttpResponseRedirect(reverse("index"))

def category(request):
    categories = Category.objects.all()
    return render(request, "auctions/category.html",{
    "categories": categories
    }) 

def listing(request,id):
    item = Listing.objects.get(pk=id)
    user = request.user
    commentsonpage = Comments.objects.filter(listing=item)
    inwatchlist = user in item.watchlist.all()
    isOwner = user.username == item.owner.username
    try:
        currentbid = Bids.objects.get(auction=item)
        return render(request, "auctions/listing.html",{
        "bidder":currentbid,
        "bid":currentbid.bid,
        "item":item,
        "watchlist": inwatchlist,
        "comments": commentsonpage,
        "isowner":isOwner
        })
    except Bids.DoesNotExist:
        return render(request, "auctions/listing.html",{
        "bid":"0.00",
        "item":item,
        "watchlist": inwatchlist,
        "comments": commentsonpage,
        "isowner":isOwner
        })   

@login_required
def watchlist(request):
    if request.method=="GET":
        user = request.user
        watchlistList=Listing.objects.filter(watchlist=user)
        return render(request, "auctions/watchlist.html",{
        "active":watchlistList,
        })

@login_required
def addwatch(request,id):
    item = get_object_or_404(Listing, pk=id)
    user = request.user
    item.watchlist.add(user)
    return HttpResponseRedirect(reverse("listing",args=(item.id, )))

@login_required
def removewatch(request,id):
    item = get_object_or_404(Listing, pk=id)
    user = request.user
    item.watchlist.remove(user)
    return HttpResponseRedirect(reverse("listing",args=(item.id, )))

@login_required
def comment(request,id):
    if request.method == "POST":
        lisitngpage= Listing.objects.get(pk=id)
        commentpage = request.POST['comment']
        writer = request.user
        Comments.objects.create(user=writer,listing=lisitngpage,comment=commentpage)
        return HttpResponseRedirect(reverse("listing",args=(id, )))

@login_required
def bid(request,id):
    if request.method == "POST":
        lisitngpage = Listing.objects.get(pk=id)
        placedbid = float(request.POST['bid'])
        seller =  lisitngpage.owner
        auctionbuyer = request.user
        originalprice = lisitngpage.price
        try:
            prebid = Bids.objects.get(auction=lisitngpage)
            previousbid = prebid.bid
            if  auctionbuyer == seller:
                messages.error(request, 'Cannot Bid on Your own Item')
                return HttpResponseRedirect(reverse("listing",args=(id, )))
            else:
                if (placedbid < originalprice) or (placedbid <= previousbid):
                    messages.error(request, 'Bid invalid, Bid higher')
                    return HttpResponseRedirect(reverse("listing",args=(id, ))) 
                else:
                    Bids.objects.filter(auction=lisitngpage).update(bid=placedbid,buyer=auctionbuyer)
                    Listing.objects.filter(pk=id).update(updated_price=placedbid)
                    messages.success(request, 'Your Bid was Successful')
                    return HttpResponseRedirect(reverse("listing",args=(id, )))

        except Bids.DoesNotExist:
            if  auctionbuyer == seller:
                messages.error(request, 'Cannot Bid on Your own Item')
                return HttpResponseRedirect(reverse("listing",args=(id, ))) 
            else:
                if (placedbid < originalprice):
                    messages.error(request, 'Bid invalid, Bid higher')
                    return HttpResponseRedirect(reverse("listing",args=(id, )))  
                else:
                    Bids.objects.create(buyer=auctionbuyer,auction=lisitngpage,bid=float(placedbid))
                    Listing.objects.filter(pk=id).update(updated_price=float(placedbid))
                    messages.success(request, 'Your Bid was Successful')
                    return HttpResponseRedirect(reverse("listing",args=(id, )))
                
def closebid(request,id):
    item = Listing.objects.get(pk=id)
    Listing.objects.filter(pk=id).update(active=False)
    messages.info(request, 'Auction has been Closed')
    return HttpResponseRedirect(reverse("listing",args=(id, )))
    
def displayclosed(request):
        if request.method=="GET":
            notActive_listing=Listing.objects.filter(active=False)
            return render(request, "auctions/index.html",{
            "active":notActive_listing,
            "title": "Closed Listing"
            })
