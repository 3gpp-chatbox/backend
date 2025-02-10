import os

def create_3gpp_structure():
    """Create the 3GPP document structure"""
    # Base directory
    base_dir = "3gpp_docs"
    
    # TS_24 specifications
    ts_24_specs = [
        "234",
        "301",
        "334",
        "341",
        "368",
        "501"
    ]
    
    try:
        # Create base directory
        os.makedirs(base_dir, exist_ok=True)
        
        # Create TS_24 directory
        ts_24_dir = os.path.join(base_dir, "TS_24")
        os.makedirs(ts_24_dir, exist_ok=True)
        
        # Create subdirectories for each specification
        for spec in ts_24_specs:
            spec_dir = os.path.join(ts_24_dir, f"TS_24.{spec}")
            os.makedirs(spec_dir, exist_ok=True)
            print(f"Created directory: {spec_dir}")
            
            # Create placeholder for PDF file
            pdf_path = os.path.join(spec_dir, f"TS_24.{spec}_v18_R18.pdf")
            if not os.path.exists(pdf_path):
                with open(pdf_path, 'w') as f:
                    f.write("# Placeholder for PDF file")
                print(f"Created placeholder: {pdf_path}")
                
        print("\nDirectory structure created successfully!")
        
    except Exception as e:
        print(f"Error creating directory structure: {str(e)}")

if __name__ == "__main__":
    create_3gpp_structure() 