from bs4 import BeautifulSoup
import requests
import pandas as pd
response_page_1 = requests.get(url="https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors/page/1")
response_page_2 = requests.get(url="https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors/page/2")
data = response_page_1.text + response_page_2.text


soup = BeautifulSoup(data, "html.parser")

major_name = [school_name.getText() for school_name in soup.select(selector=".csr-col--school-name .data-table__value")]
print(major_name)
degree_name = [degree_name.getText() for degree_name in soup.select(selector=".csr-col--school-type .data-table__value")]
print(degree_name)
# salary_element = [info.getText() for info in soup.select(selector=".csr-col--right")]
# print(salary_element)
# # I got the parent elements which have both starting and mid salary.
starting_salary_title_element = [element for element in soup.select(selector=".data-table__title") if element.getText() == "Early Career Pay:"]
# I got the child element which has "Early pay" as the title.
starting_salary_element = [salary.find_parent() for salary in starting_salary_title_element]
# Now, on the basis of child element, I've found their respective parent element.
starting_salary = [salary_element.find_all('span')[1].getText() for salary_element in starting_salary_element]
print(starting_salary)
# Now, I am finding parent element's second child element.
mid_salary_title_element = [element for element in soup.select(selector=".data-table__title") if element.getText() == "Mid-Career Pay:"]
mid_salary_element = [salary.find_parent() for salary in mid_salary_title_element]
mid_salary = [salary_element.find_all('span')[1].getText() for salary_element in mid_salary_element]
print(mid_salary)

data_dictionary = {
    "Major": major_name,
    "Degree": degree_name,
    "Starting Median Salary": [int(salary.split("$")[1].replace(",", "")) for salary in starting_salary],
    "Mid-Career Median Salary": [int(salary.split("$")[1].replace(",", "")) for salary in mid_salary]
}

df = pd.DataFrame(data_dictionary)
df.to_csv("Exploring Post Graduate Salary.csv")