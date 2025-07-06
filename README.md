# ultifresh-scraper
# Ultifresh Product Inventory Scraper

This Python script extracts inventory data from [Ultifresh Malaysia](https://ultifresh.com.my) product pages and saves the results to an Excel workbook.

It automatically:
- Loops through product pages (e.g. `/productdetail/1`, `/productdetail/2`, etc.)
- Handles different table structures (each product may have different headers)
- Writes each product's inventory table to a separate Excel sheet
