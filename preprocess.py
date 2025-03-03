import pdfplumber  # Library for extracting data from PDFs


def pdf_to_markdown(pdf_path, markdown_path):
    # Open the PDF file using pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        markdown_text = ""  # Initialize empty string to store all markdown content
        
        # Iterate through each page in the PDF
        # enumerate(pdf.pages, 1) starts page numbering from 1 instead of 0
        for page_num, page in enumerate(pdf.pages, 1):
            # Extract text while preserving layout (spacing and positioning)
            text = page.extract_text(layout=True)
            
            # Find and process all tables on the current page
            tables = page.extract_tables()
            for table in tables:
                try:
                    # Clean up the table data:
                    # 1. Replace None values with empty strings
                    # 2. Convert all cells to strings
                    # This creates a new 2D array with clean data
                    clean_table = [[str(cell or '') for cell in row] for row in table]
                    
                    # Create markdown table format:
                    # 1. First row (headers)
                    markdown_table = "\n|" + "|".join(clean_table[0]) + "|\n"
                    # 2. Separator row (dashes)
                    markdown_table += "|" + "|".join(["---"] * len(clean_table[0])) + "|\n"
                    # 3. Data rows
                    for row in clean_table[1:]:
                        markdown_table += "|" + "|".join(row) + "|\n"
                    
                    # Create a string representation of the original table
                    # This is used to find and replace the table in the original text
                    original_table_text = "".join(
                        " ".join(str(cell or '') for cell in row) 
                        for row in table
                    )
                    
                    # Replace the original table text with the markdown version
                    text = text.replace(original_table_text, markdown_table)
                    #Exmaple output: 
                    #|Column1|Column2|
                    #|---|---|
                    #|Data1|Data2|
                    #|Data3|Data4|
                    #
                    #More regular text
                    

                except Exception as e:
                    # If there's an error processing a table, print warning and continue
                    print(f"Warning: Failed to process table: {str(e)}")
                    continue
            
            # Add the processed text (including converted tables) to the markdown content
            markdown_text += text + "\n\n"
            
            # Add a horizontal rule as a page separator
            markdown_text += "---\n\n"
    
    # Write the final markdown content to a file
    with open(markdown_path, "w", encoding="utf-8") as md:
        md.write(markdown_text)

        # ... existing code ...

# Add this at the bottom of the file:
if __name__ == "__main__":
    # Replace these paths with your actual PDF and output markdown file paths
    input_pdf = "data/TS 24.501.pdf"
    output_markdown = "data/TS_24.501.md"
    
    pdf_to_markdown(input_pdf, output_markdown)