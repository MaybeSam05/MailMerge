import csv
import sys

# structure of csv 
# email , [parameter1], [parameter2], ...


# manual input: 
# user email, email key, subject, body

def main():
    with open('input.csv', 'r') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)
        parameters = headers[1:] # all the parameters are here


        # Process each row
        for row in csv_reader:
            if len(row) > 0:  # Check if row is not empty
                email = row[0]  # First column is email
                parameters = row[1:]  # Remaining columns are parameters

if __name__ == "__main__": 
    main()