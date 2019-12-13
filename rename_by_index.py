#!/usr/bin/python3
import os
import argparse

parser = argparse.ArgumentParser(description="Renames images by index and creates new csv")
parser.add_argument("dataCsv", help="Input csv file")
parser.add_argument("imgDir", help="Directory containing images")
parser.add_argument("-i", "--index", dest="startIndex", type=int, default=0, help="Starting index (= name of first image)")
parser.add_argument("-p", "--prefix", dest="imgPrefix", type=str, default="", help="Prefix to prepend to image names")
parser.add_argument("-path", "--path", dest="imgPath", type=str, default="", help="Paths to images in CSV (e.g. passing \"../training_images/\" would generate \"../training_images/0.jpg\" in CSV)")
parser.add_argument("-rh", "--remove_header", dest="removeHeader", action="store_true", default=False, help="Flag to remove header row (first line) of CSV")
parser.add_argument("-rq", "--remove_quotes", dest="removeQuotes", action="store_true", default=False, help="Flag to remove all quotes from CSV")
parser.add_argument("-cf", "--convert_floats", dest="convertFloats", action="store_true", default=False, help="Flag to convert floating-point bbox coordinates to integers")
args = parser.parse_args()

def main():
	csv_path_and_name = os.path.splitext(args.dataCsv)[0]
	csv_ext = args.dataCsv.split(".")[-1]
	output_file = open(os.path.join(csv_path_and_name + "_new" + "." + csv_ext), "w+")

	i = args.startIndex
	removeHeader = args.removeHeader
	with open(args.dataCsv, "r") as data_csv:
		for line in data_csv:
			if(i == args.startIndex and removeHeader):
				removeHeader = False
				continue
		
			line = line.replace("\"", "")
			
			# Read "old" line from CSV
			lineParts = line.split(",")

			#Get parts of image name
			oldImgName = lineParts[0]
			oldImgExt = lineParts[0].split(".")[-1]
			oldImgPath = os.path.join(args.imgDir, oldImgName)
			newImgName = args.imgPrefix + str(i) + "." + oldImgExt
			new_csvImgPath = os.path.join(args.imgPath, newImgName)
			new_realImgPath = os.path.join(args.imgDir, newImgName)

			# Create & write "new" line in output CSV
			newLineParts = [new_csvImgPath]
			for oldLinePart in lineParts[1:]:
				if(args.convertFloats):
					try:
						newLineParts.append(str(int(float(oldLinePart))))
					except ValueError:
						newLineParts.append(oldLinePart)
				else:
					newLineParts.append(oldLinePart)
			outputLine = ",".join(newLineParts)
			output_file.write(outputLine)

			# Rename image
			os.rename(oldImgPath, new_realImgPath)

			i += 1

if(__name__ == "__main__"):
	main()
