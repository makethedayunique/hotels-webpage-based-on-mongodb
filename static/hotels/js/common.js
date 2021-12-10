function getCSRFToken() {
    let cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      let c = cookies[i].trim();
      if (c.startsWith("csrftoken=")) {
        return c.substring("csrftoken=".length, c.length);
      }
    }
    return "unknown";
  }

function changeArea(country, city) {
  $.ajax({
    type: "POST",
    url: "/hotels/home/pages",
    data: {
      "country" : country,
      "city" : city,
      "csrfmiddlewaretoken" : getCSRFToken()
    },
    dataType: "json",
    success: function(json) {
        $("#id_page_num").val(json["page_count"]);
        $("#id_country_li").text(country);
        $("#id_city_li").text(city);
        // Set all the features to be unchecked
        $("#id-property-checkboxes div div input").prop("checked", false);
        $("#id-prices-checkboxes div div input").prop("checked", false);
        $("#id-amenities-checkboxes div div input").prop("checked", false);
        $("#id-beds-checkboxes div div input").prop("checked", false);
        // Get the 1st page
        getPage(1);
        var pages = parseInt(json["page_count"]);

        $("#id_pagination").empty();
        $("#id_pagination").append('<a onclick="lastpage()">&laquo;</a>');
        
        if (pages > 10) {
          pages = 10;
        }
        var index = 1;
        while (index <= pages) {
          if (index == 1) {
            $("#id_pagination").append('<a class="active" onclick="setPage(' + index + ')">' + index + "</a>");
          } else {
            $("#id_pagination").append('<a onclick="setPage(' + index + ')">' + index + "</a>");
          }
          
          index = index + 1;
        }
        
        $("#id_pagination").append('<a onclick="nextpage()">&raquo;</a>');
    },
    error: function(json) {
        $("#id_pagination").after(json["message"]);
    }
  })
}

function filterByFeatures() {
  // Collect all the features that are checked
  var country = $("#id_country_li").text();
  var city = $("#id_city_li").text();
  var property_types = $("#id-property-checkboxes div div label");
  var prices = $("#id-prices-checkboxes div div label");
  var amenities = $("#id-amenities-checkboxes div div label");
  var beds = $("#id-beds-checkboxes div div label");
  var selected_property = [];
  var selected_prices = [];
  var selected_amenities = [];
  var selected_beds = [];
  $.each(property_types, function() {
    if ($(this).children().first().is(':checked')) {
      selected_property.push($(this).text());
    }
  });
  $.each(prices, function() {
    if ($(this).children().first().is(':checked')) {
      selected_prices.push($(this).text());
    }
  });
  $.each(amenities, function() {
    if ($(this).children().first().is(':checked')) {
      selected_amenities.push($(this).text());
    }
  });
  $.each(beds, function() {
    if ($(this).children().first().is(':checked')) {
      selected_beds.push($(this).text());
    }
  });
  return {
    country,
    city,
    selected_property,
    selected_prices,
    selected_amenities,
    selected_beds
  }
}

function featureClick() {
  // Get the first page that meet the filters
  getPage(1);
  // Get the page number of the filtered data
  var features = filterByFeatures();
  let country = features.country;
  let city = features.city;
  let property_type = features.selected_property;
  let amenities = features.selected_amenities;
  let beds = features.selected_beds;
  let prices = features.selected_prices;
  $.ajax({
      type: "POST",
      url: "/hotels/home/filters-pages",
      data: {
          "csrfmiddlewaretoken" : getCSRFToken(),
          "country" : country,
          "city" : city,
          "property_type" : property_type,
          "amenities" : amenities,
          "beds" : beds,
          "prices" : prices
      },
      dataType: "json",
      success: function(json) {
        // Set the new maximum pages and update the pagination
        var pages = parseInt(json["page_count"]);
        // Set the hidden input value
        $("#id_page_num").val(json["page_count"]);
        // Update the pagination
        $("#id_pagination").empty();
        $("#id_pagination").append('<a onclick="lastpage()">&laquo;</a>');
        
        if (pages > 10) {
          pages = 10;
        }
        var index = 1;
        while (index <= pages) {
          if (index == 1) {
            $("#id_pagination").append('<a class="active" onclick="setPage(' + index + ')">' + index + "</a>");
          } else {
            $("#id_pagination").append('<a onclick="setPage(' + index + ')">' + index + "</a>");
          }
          
          index = index + 1;
        }
        
        $("#id_pagination").append('<a onclick="nextpage()">&raquo;</a>');
      },
      error: function(json) {
        $("#id_pagination").after(json["responseJSON"]["message"]);
      }
  });
}