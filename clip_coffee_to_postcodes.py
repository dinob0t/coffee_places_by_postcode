import geojson 
import json
import csv
import ast

def point_in_poly(x,y,poly):

    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside


json_data = open('man_brook_postcodes.json')
man_brook = json.load(json_data)
json_data.close()


man_brook_features = man_brook['features']

post_dict_count = {}
post_dict_mean = {}
post_dict_price = {}
count = 0
with open('../coffee_map/data.csv', 'rb') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        row_line = row
        if count >0 and row_line[0]:
            cur_lat = ast.literal_eval(row_line[4])
            cur_lon = ast.literal_eval(row_line[5]) 
            for polys in man_brook_features:
                cur_poly = polys['geometry']['coordinates'][0]
                test_poly = [tuple(l) for l in cur_poly]
                if point_in_poly(cur_lon,cur_lat,test_poly):
                    cur_post = polys['properties']['postcode']
                    break
            if cur_post not in post_dict_count.keys():
                post_dict_count[cur_post] = 1 
                post_dict_mean[cur_post] = ast.literal_eval(row_line[0])
            else:
                post_dict_count[cur_post] +=1
                post_dict_mean[cur_post] += ast.literal_eval(row_line[0])
        count +=1

my_feature_list = []
for postcodes in man_brook_features:
    cur_code = postcodes['properties']['postcode']
    cur_poly =  postcodes['geometry']['coordinates'][0]
    my_poly = geojson.Polygon([[tuple(l) for l in cur_poly]])
    prop_dict = {}
    prop_dict['postcode'] = cur_code
    prop_dict['area'] = postcodes['properties']['area']
    
    if cur_code in post_dict_count.keys():
        prop_dict['count'] = post_dict_count[cur_code]
        mean_score = float(post_dict_mean[cur_code]) /float(post_dict_count[cur_code])  
    else:
        prop_dict['store count'] = 0
        mean_score = 0
    mean_str = str(mean_score)
    print mean_str
    prop_dict['mean score'] = mean_str[:3]
    if mean_score <3.84534161491:
        prop_dict['fill'] = "#0066FF"
        prop_dict['stroke-color'] = "#0066FF"
    elif mean_score <3.92424242424:
        prop_dict['fill'] = "#66FF99"
        prop_dict['stroke-color'] = "#66FF99"
    elif mean_score < 4.060471698115:
        prop_dict['fill'] = "#FFCC66"
        prop_dict['stroke-color'] = "#FFCC66"
    else:
        prop_dict['fill'] = "#FF0000"
        prop_dict['stroke-color'] = "#FF0000"
    prop_dict['fill-opacity'] = 0.5


    my_feature = geojson.Feature(geometry=my_poly,properties = prop_dict)
    my_feature_list.append(my_feature)


my_feature_coll = geojson.FeatureCollection(my_feature_list )

dump = geojson.dumps(my_feature_coll, sort_keys=True)

with open("man_brook_postcodes_coffee_score.json", "w") as outfile:
    json.dump(my_feature_coll, outfile, indent=4)



