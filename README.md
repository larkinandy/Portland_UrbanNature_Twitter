# Portland_UrbanNature_Twitter
Scripts for downloading, processing, and analyzing nature related tweets from Portland, OR in 2017.  
Author: Andrew Larkin.

**Background:** <br>
Urban nature has many health benefits, and there are many hpothesized pathways of action (e.g. exercise, community, beauty).  Estimating utilization and impacts of each pathway is difficult using traditional greenspace meaures (e.g. satellites).  This project is designed to capture and estimate community level utilizations of specific green space pathways and compare estimates to traditional green space measures. 

**Files:** 
1. PDX_Nature_Example_2017.csv - 10 censored example tweets downloaded from the Twitter API datastream and analyzed in the scripts.
2. Portland_Metro.zip - zip file containing ArcGIS shapefiles of the Portland, OR metropolitan region.  Used in zonal statistics to estimate average EVI for the Portland, OR metrpolitan region.  
3. Extract EVI - Estimate average EVI for Portland, OR for all rasters in a set.  
4. Calc_Weekly_TFIDF - Calculate weekly TF-IDF and partition tweets into weekly sets.  
5. Calc_Word_Association - Calculate topic word frequencies.
6. Vader - Calculate weekly sentiment scores using the Python NLTK Vader algorithm.

This project is a combination of my MPH culminating experience project at George Washington University, Social Media Analytics course at Johns Hopking University, and continuing reserach into novel data streams for public health at Oregon State University.  Perry Hystad, Christina Hemminger, and Ian McCulluh contributed to the research described here.
