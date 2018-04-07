import pandas as pd
import csv


def filter_business_data():             # Filtering business which fall under category_array specified below
    category_array = ["restaurants", "food", "nightlife", "bars", "sandwiches", "fast food", "pizza",
                      "american (traditional)", "coffee & tea", "hotels & travel", "italian", "burgers",
                      "breakfast & brunch", "mexican", "chinese", "american (new)", "specialty food", "bakeries",
                      "cafes", "hotels", "desserts", "ice cream & frozen yogurt", "japanese", "chicken wings", "pubs",
                      "seafood", "salad", "sushi bars", "caterers", "sports bars", "beer", "wine & spirits",
                      "mediterranean", "barbeque", "canadian (new)", "steakhouses", "lounges", "indian", "thai",
                      "diners", "wine bars", "middle eastern", "cocktail bars", "greek", "french", "vietnamese",
                      "vegetarian", "local flavor", "buffets", "food delivery services", "korean", "soup",
                      "food trucks", "gluten-free", "vegan", "donuts", "hot dogs", "bagels", "caribbean", "gastropubs",
                      "german", "breweries", "meat shops", "halal", "imported food", "chocolatiers & shops",
                      "tea rooms", "british", "fish & chips", "noodles", "beer bar", "bubble tea", "cupcakes",
                      "food stands", "hawaiian", "soul food", "chicken shop", "dim sum", "cajun/creole", "portuguese",
                      "bed & breakfast", "pawn shops", "shaved ice", "seafood markets", "spanish", "cheesesteaks",
                      "turkish", "irish", "lebanese", "cheese shops", "taiwanese", "custom cakes", "gay bars", "ramen",
                      "persian/iranian", "delicatessen", "bistros", "wineries", "tacos", "brasseries",
                      "do-it-yourself food", "african", "poutineries", "falafel", "wraps", "afghan", "pan asian",
                      "szechuan", "kebab", "beer gardens", "scottish", "cantonese", "personal chefs", "ethiopian",
                      "moroccan", "arabian", "belgian", "argentine", "smokehouse", "mongolian", "colombian",
                      "bartenders", "cambodian", "sugaring", "cambodian", "food tours", "new mexican cuisine",
                      "wine tasting room", "sri lankan", "hungarian", "indonesian", "brewpubs", "singaporean",
                      "bangladeshi", "ukrainian", "coffeeshops", "south african", "dominican", "serbo croatian",
                      "oxygen bars", "scandinavian", "laotian", "austrian", "tiki bars", "bavarian", "egyptian",
                      "marinas", "eatertainment", "burmese", "dinner theater"]
    business_data = pd.read_csv("yelp_business.csv")
    with open("yelp_business_filter.csv", 'wb') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(
            ["business_id", "name", "neighborhood", "address", "city", "state", "postal_code", "latitude", "longitude",
             "stars", "review_count", "is_open", "categories"])
        for index, row in business_data.iterrows():
            for category in category_array:
                if (category in row['categories'].lower()):
                    writer.writerow(row)
                    break


def filter_data(filename,headerarray):  # Used to filter data which don't belong to restaurants
    business_data = pd.read_csv("yelp_business_test.csv")
    business_id_list = business_data['business_id'].tolist()
    data = pd.read_csv(filename+".csv", low_memory=False)
    with open(filename+"_filtered"+".csv",'wb') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(headerarray)
        for index, row in data.iterrows():
            if (row['business_id']) in business_id_list:
                writer.writerow(row)


# filter_business_data()
filter_data("yelp_business_attributes",["business_id","AcceptsInsurance","ByAppointmentOnly","BusinessAcceptsCreditCards","BusinessParking_garage","BusinessParking_street","BusinessParking_validated","BusinessParking_lot","BusinessParking_valet","HairSpecializesIn_coloring","HairSpecializesIn_africanamerican","HairSpecializesIn_curly","HairSpecializesIn_perms","HairSpecializesIn_kids","HairSpecializesIn_extensions","HairSpecializesIn_asian","HairSpecializesIn_straightperms","RestaurantsPriceRange2","GoodForKids","WheelchairAccessible","BikeParking","Alcohol","HasTV","NoiseLevel","RestaurantsAttire","Music_dj","Music_background_music","Music_no_music","Music_karaoke","Music_live","Music_video","Music_jukebox","Ambience_romantic","Ambience_intimate","Ambience_classy","Ambience_hipster","Ambience_divey","Ambience_touristy","Ambience_trendy","Ambience_upscale","Ambience_casual","RestaurantsGoodForGroups","Caters","WiFi","RestaurantsReservations","RestaurantsTakeOut","HappyHour","GoodForDancing","RestaurantsTableService","OutdoorSeating","RestaurantsDelivery","BestNights_monday","BestNights_tuesday","BestNights_friday","BestNights_wednesday","BestNights_thursday","BestNights_sunday","BestNights_saturday","GoodForMeal_dessert","GoodForMeal_latenight","GoodForMeal_lunch","GoodForMeal_dinner","GoodForMeal_breakfast","GoodForMeal_brunch","CoatCheck","Smoking","DriveThru","DogsAllowed","BusinessAcceptsBitcoin","Open24Hours","BYOBCorkage","BYOB","Corkage","DietaryRestrictions_dairy-free","DietaryRestrictions_gluten-free","DietaryRestrictions_vegan","DietaryRestrictions_kosher","DietaryRestrictions_halal","DietaryRestrictions_soy-free","DietaryRestrictions_vegetarian","AgesAllowed","RestaurantsCounterService"])
# filter_data("yelp_business_hours",["business_id","monday","tuesday","wednesday","thursday","friday","saturday","sunday"])
# filter_data("yelp_checkin",["business_id","weekday","hour","checkins"])
# filter_data("yelp_tip",['text','date','likes','business_id','user_id'])