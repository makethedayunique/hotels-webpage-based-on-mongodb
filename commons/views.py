from django.http import response
from django.http.response import HttpResponse
from django.shortcuts import redirect, render

from commons.querys_mongodb import Mongocessor
import json

# Create your views here.

DEFAULT_COUNTRY = "United States"
DEFAULT_CITY = "New York, NY"
mongocessor = Mongocessor()

def hotels_page_display(request):
    if request.method == "GET":
        context = {}
        context["span"] = "global"
        # mongocessor = Mongocessor()
        context["pages"] = max(0, (mongocessor.query_common_size(country=DEFAULT_COUNTRY, city=DEFAULT_CITY) - 1) // mongocessor.PAGE_SIZE + 1)
        context["initial_pages"] = range(1, min(10, context["pages"]))
        # Set country and city
        context["country"] = DEFAULT_COUNTRY
        context["city"] = DEFAULT_CITY

        context["hotels"] = mongocessor.query_common_page(1, context["country"], context["city"])  # First Page
        context["feature_grid"] = mongocessor.query_filters_statistics()

        return render(request, "hotels/products_list.html", context)
    else:
        page = int(request.POST["page"])
        country = request.POST["country"]
        city = request.POST["city"]
        property_type = request.POST.getlist("property_type[]")
        amenities = request.POST.getlist("amenities[]")
        prices = request.POST.getlist("prices[]")
        beds = request.POST.getlist("beds[]")
        
        try:
            item_array = mongocessor.query_filters_page(page=int(page), country=country, city=city,
                                                        property_types=property_type, prices=prices, amenities=amenities,
                                                        beds=beds)
        except:
            message = "Failed to Load the content, please try again!"
            alert_html = hotels_page_error_helper(message=message)
            response_data = {"html": alert_html}
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)
        html = "".join([hotels_page_display_helper(item) for item in item_array])
        response_data = {"html": html}
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)

def hotels_page_get_count(request):
    if request.method == "POST":
        country = request.POST["country"]
        city = request.POST["city"]
        context = {}
        try:
            context["page_count"] = max(1, (mongocessor.query_common_size(country, city) - 1) // mongocessor.PAGE_SIZE + 1)
        except:
            message = "Failed to get data"
            return HttpResponse(json.dumps({"message":hotels_page_error_helper(message=message)}), content_type="application/json", status=400)
        return HttpResponse(json.dumps(context), content_type="application/json", status=200)
    else:
        redirect("hotels_page_display")

def hotels_page_get_count_filters(request):
    if request.method == "POST":
        country = request.POST["country"]
        city = request.POST["city"]
        property_type = request.POST.getlist("property_type[]")
        amenities = request.POST.getlist("amenities[]")
        prices = request.POST.getlist("prices[]")
        beds = request.POST.getlist("beds[]")
        context = {}
        # try:
        context["page_count"] = max(1, (mongocessor.query_filters_size(country, city, property_type,
                                                                        prices, amenities, beds) - 1) // mongocessor.PAGE_SIZE + 1)
        # except:
        #     message = "Failed to get data"
        #     response_error = {"message" : hotels_page_error_helper(message)}
        #     return HttpResponse(json.dumps(response_error), content_type="application/json", status=400)

        return HttpResponse(json.dumps(context), content_type="application/json", status=200)
    else:
        redirect("hotels_page_display")


def hotels_page_error_helper(message):
    alert_html = '<div class="col-md-9">' + \
                 '<div class="alert alert-danger alert-dismissible" role="alert">' + message + \
                 '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>' + \
                 '</div>'
    return alert_html

def hotels_page_display_helper(item):
    html = '<div class="col-md-4 grid-stn simpleCart_shelfItem" style="height: 20vw;">' + \
           '<div class="ih-item square">' + \
           '<div class="bottom-2-top">' + \
           '<div class="img"><img src="' + item.picture_url + '" alt="/" class="gri-wid" style="width: 20vw;height: 15vw;"></div>' + \
           '<div class="info">' + \
           '<div class="pull-left styl-hdn">' + \
           '<h3>' + item.name + '</h3>' + \
           '</div>' + \
           '<div class="pull-right styl-price">' + \
           '<p><a class="item_add">' + \
           '<span class=" item_price">$' + str(item.price) + '/night</span></a></p>'
    
    if item.review_scores_rating:
        html += '<div class="pull-right">' + \
           '<span class="item_price"><i class="bi bi-star-fill" style="font-size:1vw"></i></span>' + \
           '<span style="font-size: 1vw;">' + '<b>' + str(item.review_scores_rating) + '</b> ' + '(' + str(item.number_of_reviews) + 'Reviews)' + '</span></div>'
    
    html += '<div class="pull-right" style="font-size: 1vw;">' + \
            '<b>' + str(item.bedrooms) + 'Rooms/' + str(item.beds) + 'Beds</b></div>' + \
            '</div>' + \
            '<div class="clearfix"></div>' + \
            '</div></div></div>' + \
            '<div class="quick-view">' + \
            '<a href="single.html">Quick view</a>' + \
            '</div></div>'

    return html