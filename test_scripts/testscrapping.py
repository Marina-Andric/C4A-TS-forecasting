import pandas as pd

tables = pd.read_html("http://www.espn.com/college-sports/football/recruiting/databaseresults/_/sportid/24/class/2006/sort/school/starsfilter/GT/ratingfilter/GT/statuscommit/Commitments/statusuncommit/Uncommited", header=0)

print (tables[0])

# print (tables[0].to_json(orient='records'))
