# P2_OC_Market_Analysis

Project title : 
      Web book scraping program.

Project description
  
  Use of the code : 
  
  Scraping code made for the Books Online company and made to only scrap data for "http://books.toscrape.com/website".
  This program will scrap all required and useful book data such as book url, book title, Universal Product Code, prices (inc and exc taxes), quantity available, 
  rating, book description, book category, image.

  It will create one repository per book category ({category} "folder extract). In each repository, there is :

  1. a CSV (Comma-separated values) file with headers (required data) and ligns (scraped data, one lign per book),
  2. book images stored in jpg.
  
  Packages used (Modules(m)/library(l)): 
      
  csv (m): CSV File Reading and Writing
  requests (m) 2.28.2 :  HTTP library for the Python programming language.
  os (m): Miscellaneous operating system interfaces
  re (m): Regular expression operations
  bs4 (l), BeautifulSoup (m) 4.11.2 : parsing of HTML and XML documents
  urllib.parse (l), urljoin (m) 1.26.14 : Construct a full (“absolute”) URL by combining a “base URL” (base) with another URL (url)
  utils (l), clinks (m) : function created. Clean a string list by removing/replacing typefaces by others. 
  
  Future of the code : 
      
  This is my first code and some errors may appear. Please send an email to valentin.simioni@outlook.com if there are things to fix.
  Some implementations would be useful ..
      
  How to install and Run the project :

  1. Clone the repository
  2. Install requirements (pip install -r requirements.txt)
  3. Start the program (python main.py)

Credits : 

  Ait-Mlouk Addi : mentor, participated for the code improvement.
