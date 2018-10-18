# Portland_UrbanNature_Twitter
Scripts for downloading, processing, and analyzing nature related tweets from Portland, OR in 2017.  <br> <br>
**Author:** [Andrew Larkin](https://www.linkedin.com/in/andrew-larkin-525ba3b5/) <br>
**Affiliation:** [Oregon State University, College of Public Health and Human Sciences](https://health.oregonstate.edu/) <br>
**Date Created:** April 11, 2018

**Background:** <br>
Urban nature has many health benefits, and there are many hpothesized pathways of action (e.g. exercise, community, beauty).  Estimating utilization and impacts of each pathway is difficult using traditional greenspace meaures (e.g. satellites).  This project is designed to capture and estimate community level utilizations of specific green space pathways and compare estimates to traditional green space measures. 

**Files:** 

1. **[Portland_Metro.zip](https://github.com/larkinandy/Portland_UrbanNature_Twitter/blob/master/Portland_Metro.zip)** - zip file containing ArcGIS shapefiles of the Portland, OR metropolitan region.  Used in zonal statistics to estimate average EVI for the Portland, OR metrpolitan region.  
2. **Extract EVI** - Estimate average EVI for Portland, OR for all rasters in a set.  
3. **[Calc_Weekly_TFIDF](https://github.com/larkinandy/Portland_UrbanNature_Twitter/blob/master/Calc_Weekly_TFIDF.py)** - Calculate weekly TF-IDF and partition tweets into weekly sets.  
4. **[Calc_Word_Associations.py](https://github.com/larkinandy/Portland_UrbanNature_Twitter/blob/master/Calc_Word_Associations.py)** - Calculate topic word frequencies.
5. **[Vader.py](https://github.com/larkinandy/Portland_UrbanNature_Twitter/blob/master/Vader.py)** -Calculate sentiment scores using the Python NLTK Vader algorithm.

**TODO:**

[ ] add Extract EVI.py script <br>
[X] add Vader.py script 


**History:** <br>
This project is a combination of my [MPH culminating experience project at George Washington University](https://github.com/larkinandy/MPH-Culminating-Experience), Social Media Analytics course at Johns Hopkins University, and continuing reserach into novel data streams for public health at Oregon State University.  [Perry Hystad](https://health.oregonstate.edu/people/perry-hystad), [Christina Hemminger](https://publichealth.gwu.edu/departments/prevention-and-community-health/christina-heminger), and [Ian McCulluh](https://ep.jhu.edu/about-us/faculty-directory/1511-ian-mcculloh) contributed to the research described here.
