# %% [markdown]
# # PyCity Schools Analysis
# 
# - Your analysis here
#   
# ---test

# %%
# Dependencies and Setup
import pandas as pd
import numpy as np
from pathlib import Path


# File to Load (Remember to Change These)
school_data_to_load = Path("Resources_PyCitySchools/schools_complete.csv")
student_data_to_load = Path("Resources_PyCitySchools/students_complete.csv")

# Read School and Student Data File and store into Pandas DataFrames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)


# Combine the data into a single dataset.  
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])
school_data_complete.head()

# %% [markdown]
# ## District Summary

# %%
# Calculate the total number of unique schools
school_names = school_data_complete["school_name"].unique()
school_names


# %%
# Calculate the total number of unique schools
school_count = school_data ["school_name"].count()
school_count

# %%
# Calculate the total number of students
student_count = school_data_complete["student_name"].count()
student_count


# %%
# Calculate the total budget
total_budget = school_data ["budget"].sum()
total_budget

# %%
#school_data_complete.describe()

# %%
#school_data_complete.dtypes

# %%
# Calculate the average (mean) math score
average_math_score = school_data_complete["math_score"].mean()
average_math_score

# %%
# Calculate the average (mean) reading score
average_reading_score = student_data["reading_score"].mean()
#average_reading_score = np.mean(student_data["reading_score"])
average_reading_score

# %%
# Use the following to calculate the percentage of students who passed math (math scores greather than or equal to 70)
passing_math_count = school_data_complete[(school_data_complete["math_score"] >= 70)].count()["student_name"]
passing_math_percentage = passing_math_count / float(student_count) * 100
passing_math_percentage

# %%
# Calculate the percentage of students who passed reading (hint: look at how the math percentage was calculated)  
passing_reading_count = school_data_complete[(school_data_complete["reading_score"] >= 70)].count()["student_name"]
passing_reading_percentage = passing_math_count / float(student_count) * 100
passing_reading_percentage

# %%
# Use the following to calculate the percentage of students that passed math and reading
passing_math_reading_count = school_data_complete[
    (school_data_complete["math_score"] >= 70) & (school_data_complete["reading_score"] >= 70)
].count()["student_name"]
overall_passing_rate = passing_math_reading_count /  float(student_count) * 100
overall_passing_rate

# %%
# Create a high-level snapshot of the district's key metrics in a DataFrame
district_summary = pd.DataFrame(
    {"Total Schools":[school_count],
     "Total Students":[student_count],
     "Total Budget":[total_budget],
     "Average Math Score":[average_math_score],
     "Average_Reading_Score":[average_reading_score],
     "% Passing Math":[passing_math_percentage],
     "% Passing Reading":[passing_reading_percentage],
     "% Overall Passing":[overall_passing_rate]
     })

# Formatting
district_summary["Total Students"] = district_summary["Total Students"].map("{:,}".format)
district_summary["Total Budget"] = district_summary["Total Budget"].map("${:,.2f}".format)
district_summary["Average Math Score"] = district_summary["Average Math Score"].map("{:.0f}".format)
district_summary["% Passing Math"] = district_summary["% Passing Math"].map("{:.0f}%".format)
district_summary["Average_Reading_Score"] = district_summary["Average_Reading_Score"].map("{:.0f}".format)
district_summary["% Passing Reading"] = district_summary["% Passing Reading"].map("{:.0f}%".format)
district_summary["% Overall Passing"] = district_summary["% Overall Passing"].map("{:.0f}%".format)

# Display the DataFrame
district_summary

# %% [markdown]
# ## School Summary

# %%
#grouped_by_school = school_data_complete.groupby(['school_name'])

# %%
# Use the code provided to select all of the school types
school_types = school_data_complete.groupby(['school_name'])["type"].unique().str.join(', ')



# %%
# Calculate the total student count per school
per_school_counts = school_data_complete["school_name"].value_counts()

# %%
# Calculate the total school budget and per capita spending per school
per_school_budget = school_data_complete.groupby(['school_name'])["budget"].median()
per_school_capita = per_school_budget / per_school_counts


# %%
school_data_complete.columns

#grouped_by_school.count().head(15)

# %%
# Calculate the average test scores per school

per_school_math = school_data_complete.groupby(['school_name'])['math_score'].mean()
per_school_reading = school_data_complete.groupby(['school_name'])['reading_score'].mean()


# %%
# Calculate the number of students per school with math scores of 70 or higher
students_passing_math = school_data_complete[school_data_complete["math_score"]>=70]
#school_students_passing_math
school_students_passing_math = students_passing_math.groupby(["school_name"]).size()


# %%
# Calculate the number of students per school with reading scores of 70 or higher
students_passing_reading = school_data_complete[school_data_complete["reading_score"]>=70]
#school_students_passing_reading
school_students_passing_reading = students_passing_reading.groupby(["school_name"]).size()


# %%
# Use the provided code to calculate the number of students per school that passed both math and reading with scores of 70 or higher
students_passing_math_and_reading = school_data_complete[
    (school_data_complete["reading_score"] >= 70) & (school_data_complete["math_score"] >= 70)
]
school_students_passing_math_and_reading = students_passing_math_and_reading.groupby(["school_name"]).size()
#school_students_passing_math_and_reading.head(15)

# %%
# Use the provided code to calculate the passing rates
per_school_passing_math = school_students_passing_math / per_school_counts * 100
#per_school_passing_math


# %%
per_school_passing_reading = school_students_passing_reading / per_school_counts * 100
#per_school_passing_reading

# %%
overall_passing_rate = school_students_passing_math_and_reading / per_school_counts * 100
#overall_passing_rate

# %%
# Create a DataFrame called `per_school_summary` with columns for the calculations above.


per_school_summary = pd.DataFrame(
    {"School Type": school_types,
     "Total Students":per_school_counts,
     "Total School Budget":per_school_budget,
     "Per Student Budget": per_school_capita,
     "Average Math Score":per_school_math,
     "Average Reading Score":per_school_reading,
     "% Passing Math":per_school_passing_math,
     "% Passing Reading":per_school_passing_reading,
     "% Overall Passing":overall_passing_rate
     })


# Formatting
per_school_summary["Total School Budget"] = per_school_summary["Total School Budget"].map("{:,.2f}".format)
per_school_summary["Per Student Budget"] = per_school_summary["Per Student Budget"].map("{:,.2f}".format)
per_school_summary["Average Math Score"] = per_school_summary["Average Math Score"].map("{:,.0f}".format)
per_school_summary["Average Reading Score"] = per_school_summary["Average Reading Score"].map("{:,.0f}".format)
per_school_summary["% Passing Math"] = per_school_summary["% Passing Math"].map("{:,.0f}".format)
per_school_summary["% Passing Reading"] = per_school_summary["% Passing Reading"].map("{:,.0f}".format)
per_school_summary["% Overall Passing"] = per_school_summary["% Overall Passing"].map("{:,.0f}".format)
# Display the DataFrame
per_school_summary.head(15)

# %% [markdown]
# ## Highest-Performing Schools (by % Overall Passing)

# %%
# Sort the schools by `% Overall Passing` in descending order and display the top 5 rows.
top_schools = per_school_summary.sort_values(by='% Overall Passing',ascending=False)
top_schools.head(5)

# %% [markdown]
# ## Bottom Performing Schools (By % Overall Passing)

# %%
# Sort the schools by `% Overall Passing` in ascending order and display the top 5 rows.
bottom_schools = per_school_summary.sort_values(by='% Overall Passing',ascending=True)
bottom_schools.head(5)

# %% [markdown]
# ## Math Scores by Grade

# %%
# Use the code provided to separate the data by grade
ninth_graders = school_data_complete[(school_data_complete["grade"] == "9th")]
tenth_graders = school_data_complete[(school_data_complete["grade"] == "10th")]
eleventh_graders = school_data_complete[(school_data_complete["grade"] == "11th")]
twelfth_graders = school_data_complete[(school_data_complete["grade"] == "12th")]

# Concatenate the individual grade level DataFrames
school_data_complete = pd.concat([ninth_graders, tenth_graders, eleventh_graders, twelfth_graders])

# Group by school_name and calculate the mean of math_score for each school
math_scores_by_grade = school_data_complete.pivot_table(values='math_score', index='school_name', columns='grade', aggfunc='mean')
# Reorder the columns
column_order = ['9th', '10th', '11th', '12th']

# Reindex the DataFrame to reorder the columns
math_scores_by_grade = math_scores_by_grade.reindex(columns=column_order)

# Minor data wrangling
math_scores_by_grade.index.name = None

# Display the DataFrame
math_scores_by_grade

# %% [markdown]
# ## Reading Score by Grade 

# %%
# Use the code provided to separate the data by grade
ninth_graders = school_data_complete[(school_data_complete["grade"] == "9th")]
tenth_graders = school_data_complete[(school_data_complete["grade"] == "10th")]
eleventh_graders = school_data_complete[(school_data_complete["grade"] == "11th")]
twelfth_graders = school_data_complete[(school_data_complete["grade"] == "12th")]

# Concatenate the individual grade level DataFrames
school_data_complete = pd.concat([ninth_graders, tenth_graders, eleventh_graders, twelfth_graders])

# Group by school_name and calculate the mean of reading_score for each school
reading_scores_by_grade = school_data_complete.pivot_table(values='reading_score', index='school_name', columns='grade', aggfunc='mean')
# Reorder the columns
column_order = ['9th', '10th', '11th', '12th']

# Reindex the DataFrame to reorder the columns
reading_scores_by_grade = reading_scores_by_grade.reindex(columns=column_order)

# Minor data wrangling
reading_scores_by_grade.index.name = None

# Display the DataFrame
reading_scores_by_grade


# %% [markdown]
# ## Scores by School Spending

# %%
# Establish the bins 
spending_bins = [0, 585, 630, 645, 680]
labels = ["<$585", "$585-630", "$630-645", "$645-680"]

# %%
# Create a copy of the school summary since it has the "Per Student Budget" 
school_spending_df = per_school_summary.copy()

# %%
# Convert the spending column to numeric data type
school_spending_df['Per Student Budget'] = school_spending_df['Per Student Budget'].astype(float)

# Use `pd.cut` to categorize spending based on the bins.
school_spending_df["Spending Ranges (Per Student)"] = pd.cut(school_spending_df['Per Student Budget'], bins=spending_bins, labels=labels)
school_spending_df

# %%
#  Calculate averages for the desired columns. 
spending_math_scores = school_spending_df.groupby("Spending Ranges (Per Student)")["Average Math Score"].mean()
print(spending_math_scores)

spending_reading_scores = school_spending_df.groupby(["Spending Ranges (Per Student)"])["Average Reading Score"].mean()
spending_passing_math = school_spending_df.groupby(["Spending Ranges (Per Student)"])["% Passing Math"].mean()
spending_passing_reading = school_spending_df.groupby(["Spending Ranges (Per Student)"])["% Passing Reading"].mean()
overall_passing_spending = school_spending_df.groupby(["Spending Ranges (Per Student)"])["% Overall Passing"].mean()

# %%

# Assemble into DataFrame
spending_summary = pd.DataFrame(
    {"Average Math Score": spending_math_scores,
    "Average Reading Score": spending_reading_scores,
    "% Passing Math": spending_passing_math,
    "% Passing Reading": spending_passing_reading,
    "% Overall Passing": overall_passing_spending
     })
# Display results
spending_summary

# %% [markdown]
# ## Scores by School Size

# %%
# Establish the bins.
size_bins = [0, 1000, 2000, 5000]
labels = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]

# %%
# Convert the spending column to numeric data type
school_spending_df['Total Students'] = school_spending_df['Total Students'].astype(float)


# Categorize the spending based on the bins
# Use `pd.cut` on the "Total Students" column of the `per_school_summary` DataFrame.

per_school_summary["School Size"] = pd.cut(school_spending_df['Total Students'], bins=size_bins, labels=labels)
school_spending_df

per_school_summary

# %%
# Calculate averages for the desired columns. 
size_math_scores = per_school_summary.groupby(["School Size"])["Average Math Score"].mean()
size_reading_scores = per_school_summary.groupby(["School Size"])["Average Reading Score"].mean()
size_passing_math = per_school_summary.groupby(["School Size"])["% Passing Math"].mean()
size_passing_reading = per_school_summary.groupby(["School Size"])["% Passing Reading"].mean()
size_overall_passing = per_school_summary.groupby(["School Size"])["% Overall Passing"].mean()

# %%
# Create a DataFrame called `size_summary` that breaks down school performance based on school size (small, medium, or large).
# Use the scores above to create a new DataFrame called `size_summary`
size_summary = pd.DataFrame(
    {"Average Math Score": size_math_scores,
    "Average Reading Score": size_reading_scores,
    "% Passing Math": size_passing_math,
    "% Passing Reading": size_passing_reading,
    "% Overall Passing": size_overall_passing
})

# Display results
size_summary

# %% [markdown]
# ## Scores by School Type

# %%
# Group the per_school_summary DataFrame by "School Type" and average the results.
average_math_score_by_type = per_school_summary.groupby(["School Type"])["Average Math Score"].mean()
average_reading_score_by_type = per_school_summary.groupby(["School Type"])["Average Reading Score"].mean()
average_percent_passing_math_by_type = per_school_summary.groupby(["School Type"])["% Passing Math"].mean()
average_percent_passing_reading_by_type = per_school_summary.groupby(["School Type"])["% Passing Reading"].mean()
average_percent_overall_passing_by_type = per_school_summary.groupby(["School Type"])["% Overall Passing"].mean()

# %%
# Assemble the new data by type into a DataFrame called `type_summary`
type_summary = pd.DataFrame(
    {"Average Math Score": average_math_score_by_type,
    "Average Reading Score": average_reading_score_by_type,
    "% Passing Math": average_percent_passing_math_by_type,
    "% Passing Reading": average_percent_passing_reading_by_type,
    "% Overall Passing": average_percent_overall_passing_by_type
})
# Display results
type_summary

# %%



