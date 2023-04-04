# sqlalchemy-challenge

This is a climate analysis on Honolulu, Hawaii to help with planning for a trip there.

Analysis and Exploring the climate data
I used Python and SQLAlchemy to do a basic climate analysis and data exploration of my climate database. I specifically used SQLAlchemy ORM queries, Pandas and Matplotlib.

I used SQLAlchemy functions to  do the following:
- connect to my SQLite database
- reflect my tables into classes, and then save references to the classes

I then Linked Python to the database by creating a SQLAlchemy session.


Precipitation Analysis

I performed a precipitation analysis and then a station analysis.

In this step I found the most recent date in the dataset.

I used that date, to get the previous 12 months of precipitation data by data querying the previous 12 months of data.

I selected only the “date” and “prcp” values.

Loaded the query results into pandas DataFrame, and set the index to the “data” column.

Sorted the DataFrame values by “date”

I managed to plot the results by using the Data Frame plot method. Then used Pandas to print the summary statistics for the precipitation data.

Station Analysis

I designed a number of queries which did the following:
- Calculate the total number of stations in the dataset.
- Find the most-active stations (that is, the stations that have the most rows) by- listing the stations and observation counts in descending order.
- Finding which station ID had the greatest number of observations.
- Using the most-active station ID, to calculate the lowest, highest and average temperatures. 

I designed a query to get the previous 12 months of temperature observation (TOBS) data by
- Filtering by the station that has the greatest number of observations.
  -  Querying the previous 12 months of TOBS data for that station.
- Ploting the results as a histogram with bins=12.
 
Designing a climate App
After my analysis I designed a Flask API based on the queries that I have developed.

See listed below the steps to be followed when using Flask to create the routes.

1. /
* Start at the homepage.
* List all the available routes.

2. /api/v1.0/precipitation
* Convert the query results to a dictionary by using date as the key and prcp as the value.
* Return the JSON representation of your dictionary.

3. /api/v1.0/stations
* Return a JSON list of stations from the dataset.

4. /api/v1.0/tobs
* Query the dates and temperature observations of the most-active station for the previous year of data.
* Return a JSON list of temperature observations for the previous year.

5. /api/v1.0/<start> and /api/v1.0/<start>/<end>
* Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
* For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
* For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
