import xml.etree.ElementTree as ET
import csv

# Load and parse the XML file
xml_file = "/home/treenut/fermented/doi_10.15454_FZHIE0-Fermentation monitoring of L. delbrueckii subsp. bulgaricus CFL1.txt-endnote.xml"  # Replace with your actual file path
tree = ET.parse(xml_file)
root = tree.getroot()

# Open CSV file for writing
csv_file = "fermentation_data.csv"
with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    # Write header
    writer.writerow(["Title", "Authors", "Year", "Keywords", "URL", "Publisher"])
    
    # Extract data from the XML structure
    for record in root.findall(".//record"):
        title = record.find(".//title").text if record.find(".//title") is not None else ""
        year = record.find(".//year").text if record.find(".//year") is not None else ""
        publisher = record.find(".//publisher").text if record.find(".//publisher") is not None else ""
        
        # Extract authors
        authors = [author.text for author in record.findall(".//authors/author")]
        authors_str = "; ".join(authors)  # Join authors into a single string
        
    
