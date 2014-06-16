import json
import geojson 


json_data = open('PostalBoundary.geojson')
man_brook = json.load(json_data)
json_data.close()


manhattan =  {'10001': 'Chelsea and Clinton',
              '10011': 'Chelsea and Clinton',
              '10018': 'Chelsea and Clinton',
              '10019': 'Chelsea and Clinton',
              '10020': 'Chelsea and Clinton',
              '10036': 'Chelsea and Clinton',         
			  '10029': 'East Harlem',
			  '10035': 'East Harlem',
			  '10010': 'Gramercy Park and Murray Hill',
			  '10016': 'Gramercy Park and Murray Hill',
			  '10017': 'Gramercy Park and Murray Hill',
			  '10022': 'Gramercy Park and Murray Hill',
	 		  '10012': 'Greenwich Village and Soho',
	 		  '10013': 'Greenwich Village and Soho',
	 		  '10014': 'Greenwich Village and Soho',
			  '10004': 'Lower Manhattan',
			  '10005': 'Lower Manhattan', 
			  '10006': 'Lower Manhattan',
			  '10007': 'Lower Manhattan',
			  '10038': 'Lower Manhattan',
			  '10280': 'Lower Manhattan',
	 		  '10002': 'Lower East Side',
	 		  '10003': 'Lower East Side',
	 		  '10009': 'Lower East Side',
	 		  '10021': 'Upper East Side',
	 		  '10028': 'Upper East Side',
	 		  '10044': 'Upper East Side',
	 		  '10075': 'Upper East Side',
	 		  '10162': 'Upper East Side',
	 		  '10065': 'Upper East Side',
	 		  '10128': 'Upper East Side',
			  '10023': 'Upper West Side',
			  '10024': 'Upper West Side',
			  '10025': 'Upper West Side',
	 		  '10031': 'Inwood and Washington Heights',
	 		  '10032': 'Inwood and Washington Heights',
	 		  '10033': 'Inwood and Washington Heights',
	 		  '10034': 'Inwood and Washington Heights',
	 		  '10040': 'Inwood and Washington Heights',
	 	 	  '10026': 'Central Harlem',
	 	 	  '10027': 'Central Harlem',
	 	 	  '10030': 'Central Harlem',
	 	 	  '10037': 'Central Harlem',
	 	 	  '10039': 'Central Harlem'}

brooklyn = {'11212': 'Central Brooklyn',	 
		    '11213': 'Central Brooklyn',
		    '11216': 'Central Brooklyn',
		    '11233': 'Central Brooklyn',
		    '11238': 'Central Brooklyn',
		    '11209': 'Southwest Brooklyn',	 
		    '11214': 'Southwest Brooklyn',
		    '11228': 'Southwest Brooklyn',
		    '11204': 'Borough Park',	 
		    '11218': 'Borough Park',
		    '11219': 'Borough Park',
		    '11230': 'Borough Park',
		    '11234': 'Canarsie and Flatlands',
		    '11236':'Canarsie and Flatlands',
		    '11239':'Canarsie and Flatlands',
		    '11223': 'Southern Brooklyn',
		    '11224': 'Southern Brooklyn',
		    '11229': 'Southern Brooklyn',
		    '11235': 'Southern Brooklyn',
		    '11201': 'Northwest Brooklyn',
		    '11205': 'Northwest Brooklyn', 
		    '11215': 'Northwest Brooklyn',
		    '11217': 'Northwest Brooklyn',
		    '11231': 'Northwest Brooklyn',
		    '11203': 'Flatbush',
		    '11210': 'Flatbush', 
		    '11225': 'Flatbush',
		    '11226': 'Flatbush',
		    '11207': 'East New York and New Lots',
		    '11208': 'East New York and New Lots',
		    '11211': 'Greenpoint',
		    '11222': 'Greenpoint',
		    '11220': 'Sunset Park', 
		    '11232': 'Sunset Park', 
		    '11206': 'Bushwick and Williamsburg',
		    '11221': 'Bushwick and Williamsburg',
		    '11237': 'Bushwick and Williamsburg'}

my_feature_list = []
for postcodes in man_brook['features']:
	cur_code = postcodes['properties']['POSTAL']
	if cur_code in manhattan.keys() or cur_code in brooklyn.keys():
		cur_poly = 	postcodes['geometry']['coordinates'][0]
		my_poly = geojson.Polygon([[tuple(l) for l in cur_poly]])
		prop_dict = {}
		prop_dict['postcode'] = cur_code
		if cur_code in manhattan.keys():
			prop_dict['area'] = manhattan[cur_code]
		elif cur_code in brooklyn.keys():
			prop_dict['area'] = brooklyn[cur_code]

		my_feature = geojson.Feature(geometry=my_poly,properties = prop_dict)
		my_feature_list.append(my_feature)


my_feature_coll = geojson.FeatureCollection(my_feature_list )

dump = geojson.dumps(my_feature_coll, sort_keys=True)

with open("man_brook_postcodes.json", "w") as outfile:
	json.dump(my_feature_coll, outfile, indent=4)
