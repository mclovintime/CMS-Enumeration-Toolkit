import csv
import argparse
from datetime import date

# argument syntax example:
# python3 sanitizer.py input1.csv input2.csv input3.csv output.txt

def main(input_files, output_file):
    websites = set()

    for input_file in input_files:
        with open(input_file, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                website = row[2]
                if website != "":
                    websites.add(website)

        with open(output_file, 'a') as outfile:
            outfile.write(("*" * 40) + "\n" + "Collected from " + input_file + " on " + str(date.today()) + '\n' + ("*" * 40) + "\n")
            for website in websites:
                outfile.write(website + '\n')

        print(f"Unique websites written to {output_file} from {input_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract unique websites from multiple CSV files')
    parser.add_argument('input_csv', nargs='+', help='The input CSV files')
    parser.add_argument('output_txt', help='The output text file')

    args = parser.parse_args()

    main(args.input_csv, args.output_txt)