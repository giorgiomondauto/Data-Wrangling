# DATA WRANGLING:
#    - Data Transformation : Discretization and Binning
#    - Data Cleaning
#    - Combining and Merging Data Sets
#    - Concatenating method
#    - String Manipulation
#    - Regular Expression
# Plotting  
# Basic Descriptive Statistics

#The dataset taken in consideration contains information about university rankings worldwide.
#Data has been provided by the 'Times higher education world university rankings', founded in 2004 (UK);
#Information is trusted by government and universities, and represents a vital resource for students, helping them choose where to study. 

#Get Started
#Recall some of the packages
import pandas as pd
import numpy as np
from pandas import Series, DataFrame

path="C:/Users/giorg/Desktop/Data Wrangling/"   
data=pd.read_csv(path+"Data1.csv")#university data (shape=(2198,13)).

#Focus the analysis on the first 100(world_rank) universities by year (2012-2015)
or_data=data.copy()  # I want to keep original data called or_data
#partition of data in two data sets: data_12_13 and data_14_15 inasmuch their classification has been done by considering different range of universities 
#for data in 2012 and 2013 the range is up to 100 universities; for data in 2014 and 2015 the range is up to 1000 universities.
#Besides, we are mostly interested in the last two datasets

data_12_13=data[:200] 
data_14_15=data[200:]

# Start to do some transformation to data_14_15 (dataset of interest) in order to better the visualisation of data. 
#Partition of the Rank Attributes in 7 different classes.
bins=[0,20,40,60,80,100,300,1000]
groups='1class,2class,3class,4class,5class,6class'
groups=groups +',lastclass'
str_class=[x.strip() for x in groups.split(",")]

data_14_15["quality_of_education"]=pd.cut(data.quality_of_education,bins,labels=str_class)
data_14_15["quality_of_faculty"]=pd.cut(data.quality_of_faculty,bins,labels=str_class) 
data_14_15["alumni_employment"]=pd.cut(data.alumni_employment,bins,labels=str_class)
data_14_15["citations"]=pd.cut(data.citations,bins,labels=str_class)
data_14_15["publications"]=pd.cut(data.publications,bins,labels=str_class)
data_14_15["influence"]=pd.cut(data.influence,bins,labels=str_class)
data_14_15["patents"]=pd.cut(data.patents,bins,labels=str_class)

 #delete column="year" because we want groupings per year and delete column="rank" because we will set it as index
 #partition in four subsets according to year
data1_14_15=data_14_15.drop(data.columns[[0,12]],axis=1) 
data_2014=DataFrame(data1_14_15.ix[range(200,300)])# university data per year 2014 (shape= (100,11))
data_2014.index=[range(1,101)]
data_2014.to_csv(path+"data_2014.csv")
data_2015=DataFrame(data1_14_15.ix[range(1199,1299)]) # university data per year 2015 (shape=(100,11))
data_2015.index=[range(1,101)]
data_2015.to_csv(path+"data_2015.csv")

data2_12_13=data_12_13.drop(data.columns[[0,12]],axis=1)
data_2012=DataFrame(data2_12_13.ix[:99]) # university data per year 2012  (shape=(100,11)) 
data_2012.index=[range(1,101)]  #index=world_rank
data_2013=DataFrame(data2_12_13.ix[range(100,200)]) # university data per year 2013 (shape=(100,11))
data_2013.index=[range(1,101)]  #index=world_rank

#Analyse missing values
np.where(data_2012.isnull())
 #output: (array([23, 34], dtype=int64), array([1, 1], dtype=int64))  # note that ix[23,34] corresponds to data_2012.ix[24,35] because I modified my index from 1
data_2012.country.ix[24]="USA"
data_2012.country.ix[35]="Canada"

np.where(data_2015.isnull())
#output :(array([91], dtype=int64), array([6], dtype=int64))   missing value in data_2015.ix[92,6]   91=>92 for the index reason
#To replace this value, we need to give a look at Data_2014. More precisely, we should verify if we can replace 
#the missing value with the corresponding value in data_2014.

data_2014.country.ix[range(70,100)] # we have three universities from Switzerald. analysing each one in order to identify the university of Geneva
#We observe that In 2014, the university of Geneva was ranked 2 in the country and 75 in the world; 
#comparing these statistics with ones of 2015 ({national_rank:3, world_rank:92}). 
pd.concat([data_2014.ix[75],data_2015.ix[92]],axis=1,keys=["2014","2015"])
#it can be deducted that there have not been huge variations which lead to consider
#University of Geneva as part of “last class”. In so doing, the  missing value is replaced  with the previous one, that is “6class”.
#Besides, the total score has decreased of only 2.04.
data_2014.ix[75]  # 6class
data_2015.ix[92,6]="6class"  #alternative way: data_2015=data_2015.replace(np.nan,"6class")

#Focus our attention on data_2015
data_2015=data_2015.rename(columns=str.upper)
data_2015.COUNTRY.value_counts() #observations on the number of universities per every country

# creation of a new variable "Continent" through the map tool. Basically each country is associated to its Continent.
my_map={'USA':"AMERICA",'Japan':"ASIA",'United Kingdom':"EUROPE",'Switzerland':"EUROPE",'France':"EUROPE",
'Canada':"AMERICA",'Israel':"ASIA",'Netherlands':"EUROPE",'Germany':"EUROPE",'Australia':"OCEANIA",'Denmark':"EUROPE",'China':"ASIA",'South Korea':"ASIA",
'Russia':"EUROPE",'Sweden':"EUROPE",'Singapore':"ASIA",'Taiwan':"ASIA",'Norway':"EUROPE",'Belgium':"EUROPE"} # I have considered Russia as part of Europe (actually is part of Eurasia which is combined continental landmass of Europe and Asia
data_2015["CONTINENT"]=data_2015.COUNTRY.map(my_map)
data_2015.CONTINENT.value_counts() 
#Alternative way with str.contains :
possible_way=data_2015.CONTINENT.str.contains("AMERICA") 
possible_way.value_counts()

# we are going to plot the Continent and Country cross tabulation.
tab_country_continent=pd.crosstab(data_2015.CONTINENT,data_2015.COUNTRY)
tab_country_continent.plot(kind="bar",stacked=True,title="Top 100 Universities in 2015",use_index=True,yticks=(np.arange(0,65,5)))
plt.savefig("tab_country_continent.pdf") #save our graph

pd.crosstab(data_2015.QUALITY_OF_EDUCATION,data_2015.ALUMNI_EMPLOYMENT,margins=True) #cross tabulation between quality of education and alumni employment attributes

# Using pd.merge in order to identify differences in world rank between 2014 and 2015.
data_2015_rank=DataFrame([np.arange(1,11,1),data_2015.INSTITUTION[:10]]).T
data_2015_rank.columns=["world_rank","institution_2015"]
data_2014_rank=DataFrame([np.arange(1,11,1),data_2014.institution[:10]]).T
data_2014_rank.columns=["world_rank","institution_2014"]
pd.merge(data_2014_rank,data_2015_rank,on="world_rank") #note that the only change is rank:10 where the Cornell University replaces Yale University. 

# Comparing data of Cornell University and Yale University in 2014 with ones in 2015 by considering the original data (or_data) in that we want to analyze
# in details the variations (if they are present) regarding each attribute
or_data_2014=DataFrame(or_data.ix[range(200,300)])# university data per year 2014 (shape= (100,11))
or_data_2014.index=[range(1,101)]

or_data_2015=DataFrame(or_data.ix[range(1199,1299)]) # university data per year 2015 (shape=(100,11))
or_data_2015.index=[range(1,101)]

# Cornell Unversity 
pd.concat([or_data_2014.ix[11],or_data_2015.ix[10]],axis=1,keys=["2014","2015"]) # there are some improvements in quality of faculty (18-->14),
#and patents (12-->11); nevertheless, we also can notice that the rank per publications,citations have decreased over the period. 
#However the quality of education presents a major weight in defining the national_rank and above all the total score which has increased of nearly 1.00 point 

# Yale University
pd.concat([or_data_2014.ix[10],or_data_2015.ix[11]],axis=1,keys=["2014","2015"]) #Yale University presents decreasing ranking in quality_of_education,
 # alumni_employment, influence, citations and patents. As a result, Yale University is ranked 9 in the national rank and 11 in the world rank in 2015. 
 
 # observations on which of the first 10 universities do not present a First class level for the following attributes: 
is_1class=DataFrame([data_2015.INSTITUTION[:10],
data_2015.QUALITY_OF_EDUCATION[:10].str.contains("1class"),data_2015.ALUMNI_EMPLOYMENT[:10].str.contains("1class"),
data_2015.INFLUENCE[:10].str.contains("1class"),data_2015.QUALITY_OF_FACULTY[:10].str.contains("1class")]).T  
data_2015.ALUMNI_EMPLOYMENT.ix[7] # University of California takes part of the first 40 universities in Employment of alumni
data_2015.INFLUENCE.ix[9]  # Princeton University is part of the first 40 universities in pubblications.

# a(n) (articulate) way to see how many universities (among the first 50) belong to a first class level per education in 2015 is to use regular expression
string_education=str(data_2015.QUALITY_OF_EDUCATION[:50])
import re
regex=re.compile("\s+")
string_education1=str(regex.split(string_education))
string_education2=re.sub(r'Categories.*$', "",string_education1)
first_class_education=re.findall("1class",string_education2)
len(first_class_education) #19
second_class_education=re.findall("2class",string_education2)
len(second_class_education) #10
#at the same way, we get {"3class":4,"4class":5,"5class":4,"6class":6,"lastclass":2}
#Check
data_2015.QUALITY_OF_EDUCATION[:50].value_counts() # ({"1class":19,"2class":10}

# I may get similar results by creating dummy variables: 
# creation of a dummy variable in order to analyze in detail the quality of faculty of the top 20 universities.
data_top_2015=data_2015[:20]
institution_faculty_2015=pd.get_dummies(data_top_2015.QUALITY_OF_FACULTY)
institution_faculty_2015.index.name="Rank"
institution_faculty_2015.columns.name="FACULTY"
# only University of Michigan belongs to the first 300 universities per faculty quality. 
# 15% belongs to 2class (20-40 first universities)  and the remaining 80% of universities (16) present an excellent level of faculty (1class). 

#Creation of a DataFrame containing the first top 10 universities in 2015 and the corresponding web pages.
institution_web_page=["http://www.harvard.edu/,https://www.stanford.edu/,http://web.mit.edu/,https://www.cam.ac.uk/,http://www.ox.ac.uk/,http://www.columbia.edu/,http://www.berkeley.edu/,http://www.uchicago.edu/,https://www.princeton.edu/main/,https://www.cornell.edu/"]
web_page=DataFrame([re.split('[,]',x) for x in institution_web_page]).T
web_page.index=[range(1,11)]
web_page.columns=["web_page"]
Details_Excellent_Universities=DataFrame([data_2015.INSTITUTION[:10],data_2015.SCORE[:10],or_data_2015.quality_of_education[:10],web_page.web_page]).T
#Write out the data frame:
Details_Excellent_Universities.to_csv(path+"top_10_universities.csv")

# summarizing the number of universities belonging to various classes according to education and faculty level.
data_2015.QUALITY_OF_EDUCATION.value_counts() 
data_2015.QUALITY_OF_FACULTY.value_counts() 
count_education=DataFrame({"quality":["1class","2class","3class","4class","5class","6class","lastclass"],"count_educat":[20,16,11,10,10,20,13]})
count_faculty=DataFrame({"quality":["1class","2class","3class","4class","5class","6class","lastclass"],"count_facul":[20,20,11,11,9,29,0]})
pd.merge(count_education,count_faculty,on="quality")

#Focus on SCORE attribute
data_2015.SCORE.describe() #min, max, range =(max-min)

#partitioning Score attribute in bins
bins=[50,60,70,80,90,100]
cut_score=pd.cut(data_2015.SCORE,bins,labels=["(50-60]","(60-70]","(70-80]","(80-90]","(90-100]"])
# Creating of Score dummy variable
dummies_cut_score=DataFrame(pd.get_dummies(cut_score)).astype("float")
dummies_cut_score.columns=["very_low_score","low_score","normal_score","good_score"," very_good_score"]

# work again on the strings. My aim is to identify how many universities are stored
# in 5 different groups previously created by manipulating strings. 

verylowscorestr1=str(dummies_cut_score.very_low_score[:50])
verylowscorestr2=str(dummies_cut_score.very_low_score[50:])
#I decided to partition the string in two substrings because
#If I considered a whole string,there would be some values that would not be taken in consideration. 
 
lowscorestr1=str(dummies_cut_score.low_score[:50])
lowscorestr2=str(dummies_cut_score.low_score[50:])

# in the following case, I don't need to partition because my values of interest ("1.0") are considered.
normalscorestr=str(dummies_cut_score.normal_score)
goodscorestr=str(dummies_cut_score.good_score)
verygoodscorestr=str(dummies_cut_score[[4]])

very_low_score1=str(re.findall("1.0",verylowscorestr1))
very_low_score1.count("1.0")#18
very_low_score2=str(re.findall("1.0",verylowscorestr2))
very_low_score2.count("1.0") #50

low_score1=str(re.findall("1.0",lowscorestr1))
low_score1.count("1.0")#16
low_score2=str(re.findall("1.0",lowscorestr2))
low_score2.count("1.0")#0
#to sum up, very_low_score = 68 and low_score=16

medium_score=str(re.findall("1.0",normalscorestr))
medium_score.count("1.0") #4
good_score=str(re.findall("1.0",goodscorestr))
good_score.count("1.0")#4
very_good_score=str(re.findall("1.0",verygoodscorestr))
very_good_score.count("1.0") #8

#summary score
summary_score=DataFrame({"Score":["very_low","low","medium","good","very_good"],"universities":[68,16,4,4,8]})
summary_score.index=["[50-60]","(60-70]","(70-80]","(80-90]","(90-100]"]
summary_score.plot(kind="bar",legend=False,title="Score Summary")

#final summary: Dataframe including the first top 10 universities from year 2012 to 2015.
final_summary=DataFrame([data_2012.institution[:10],data_2013.institution[:10],data_2014.institution[:10],data_2015.INSTITUTION[:10]]).T
final_summary.columns=["2012","2013","2014","2015"]
# save the dataframe in our path
final_summary.to_csv(path+"top_ten_2012_2015.csv")

# Finally, we would like to know the universities that have been more frequently ranked in the first 10 places from 2012 to 2015.
stringa=str(final_summary)
freq=[stringa.count("Harv"),stringa.count("Mass"),stringa.count("Stan"),stringa.count("Camb"),stringa.count("California Institute of Technology"),stringa.count("Princ"),stringa.count("Oxf"),stringa.count("Yal"),stringa.count("Colum"),stringa.count("Berk"),stringa.count("Chi"),stringa.count("Corne")]
tab_freq_univ=DataFrame({"University":["Harvard","Massachusetts","Stanford","Cambridge","California Institute of Tech","Princeton","Oxford","Yale","Columbia","Berkeley","Chicago","Cornell"],"frequency":freq})
tab_freq_univ.sort(["frequency"],ascending=False)

print 'The End\n Thanks for your attention\n  I hope you have enjoyed reading my Data Wrangling Project \n   Bibliography: http://www3.canisius.edu/~yany/python/Python4DataAnalysis.pdf \n    Giorgio Mondauto '




