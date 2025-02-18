# src/main.py
import os
import getpass
from docx import Document as DocxDocument
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
from langchain_community.graphs import Neo4jGraph
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate
import backend.doc_processor as doc_processor


# Load the Google API Key from the .env file
load_dotenv(override=True)

# Load the docx file inside data/
docx_file_path = "data/24501-j11.docx"

ollama = False


def initialize_llm():
    if ollama:
        print("Using Ollama")
        llm = ChatOllama(
            model="llama3.1",
            temperature=0,
            format="json",
        )
    else:
        print("Using Google Generative AI")
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0,
            format="json",
        )

    return llm


def create_state_flow_transformer(llm):
    """Creates a specialized transformer for state flow extraction"""
    return LLMGraphTransformer(
        llm=llm,
        additional_instructions="""
            Focus on extracting state transition information from the 3GPP procedure:
            
            1. States:
               - Identify all distinct states mentioned in the procedure
               - Include initial and final states
               - Tag states with properties like {{type: ["INITIAL", "INTERMEDIATE", "FINAL"]}}
            
            2. Transitions:
               - Identify events/triggers that cause state changes
               - Capture conditions for state transitions
               - Include timing and prerequisite conditions
            
            3. Create the following node types:
               - State nodes with properties:
                 * name: The state name
                 * type: The state type (INITIAL, INTERMEDIATE, FINAL)
                 * description: Brief description of the state
               
               - Condition nodes with properties:
                 * condition: The conditional expression
                 * type: ["GUARD", "TIMER", "EVENT"]
            
            4. Create relationships:
               - TRANSITIONS_TO: Between states, with properties:
                 * trigger: The event causing the transition
                 * condition: Any guard conditions
                 * probability: Likelihood if specified
               
               - DEPENDS_ON: Between conditions and states
               - TRIGGERS: Between events and transitions
            
            Format the output as a graph where:
            - Each state is a distinct node
            - Each condition is a distinct node
            - Edges represent transitions with their properties
            - All conditional logic is preserved in the graph structure
            """
    )


# Load document and check if it loaded successfully
doc = doc_processor.load_document(docx_file_path)

# Extract sections from the document
sections = doc_processor.extract_section_tree(doc)

paragraphs = doc_processor.extract_paragraphs(doc)

# ============== START OF PRINTING FOR DEBUGGING ==================
print(f"\nFound {len(sections)} top-level sections:")

for para in paragraphs:
    if "annex b" in para['text'].lower():
        print(para['style'])
        print(para['text'])
        print("*" * 80)


def get_section_content_length(section):
    # Get max content length from individual chunks in current section
    current_length = max((len(chunk) for chunk in section.content), default=0) if hasattr(section, 'content') else 0
    
    # Recursively get content length of subsections
    subsection_lengths = [get_section_content_length(subsec) for subsec in section.subsections]
    
    # Return the maximum length found
    return max([current_length] + subsection_lengths)

def print_section_tree(section, file, indent_level=0, parent_heading=None):
    indent = "  " * indent_level
    connector = "└─ " if indent_level > 0 else ""
    
    # Write current section info to file
    section_type = "Top Level Section" if indent_level == 0 else "Section"
    file.write(f"\n{indent}{connector}{section_type}: {section.heading}")
    file.write(f"\n{indent}{'   ' if indent_level > 0 else ''} Level: {section.level}")
    file.write(f"\n{indent}{'   ' if indent_level > 0 else ''} Number of subsections: {len(section.subsections)}")
    parent_info = f"Parent: {parent_heading}" if parent_heading else "Parent: None (Root level)"
    file.write(f"\n{indent}{'   ' if indent_level > 0 else ''} {parent_info}")
    
    # Recursively write subsections
    for subsection in section.subsections:
        print_section_tree(subsection, file, indent_level + 1, section.heading)

# Calculate largest content length across all sections and subsections
largest_content = max(get_section_content_length(section) for section in sections)

# Create output file for section tree
output_file_path = "section_tree.txt"
print(f"\nWriting section tree to {output_file_path}...")

with open(output_file_path, "w", encoding="utf-8") as f:
    f.write(f"Document Section Tree Analysis\n")
    f.write(f"Found {len(sections)} top-level sections:\n")
    f.write(f"Largest content in chars: {largest_content}\n")
    f.write("=" * 80)
    
    for section in sections:
        print_section_tree(section, f)
        f.write(f"\n{'-' * 80}\n")

print(f"Section tree has been written to {output_file_path}")

# ============== END OF PRINTING FOR DEBUGGING ==================

# Initialize Neo4j graph
graph = Neo4jGraph()

# Create Cypher constraints and indexes for better performance
graph.query("""
    CREATE CONSTRAINT state_name IF NOT EXISTS
    FOR (s:State) REQUIRE s.name IS UNIQUE
""")

graph.query("""
    CREATE CONSTRAINT condition_id IF NOT EXISTS
    FOR (c:Condition) REQUIRE c.id IS UNIQUE
""")

# Process the document in procedure-based chunks
llm = initialize_llm()
state_transformer = create_state_flow_transformer(llm)

def process_sections(sections, parent_procedure=None):
    """
    Process sections recursively, attempting to extract state flows from each section.
    Each content chunk is processed individually to avoid memory issues.
    
    Args:
        sections: List of sections to process
        parent_procedure: Name of the parent procedure for context
    """
    for section in sections:
        print(f"\nProcessing section: {section.heading}")
        
        if hasattr(section, 'content') and section.content:
            # Process each chunk individually
            for chunk_index, chunk in enumerate(section.content):
                # Create document for individual chunk
                doc = Document(
                    page_content=f"# {section.heading}\n{chunk}",
                    metadata={
                        "section": section.heading,
                        "parent_section": parent_procedure,
                        "level": section.level,
                        "chunk_index": chunk_index,
                        "total_chunks": len(section.content)
                    }
                )
                process_chunk(doc)
        
        # Recursively process subsections
        if section.subsections:
            process_sections(section.subsections, section.heading)

def process_chunk(doc):
    """
    Process an individual content chunk and add any found state flows to the graph.
    
    Args:
        doc: Document object containing a single content chunk
    """
    try:
        chunk_info = f"chunk {doc.metadata['chunk_index'] + 1}/{doc.metadata['total_chunks']}"
        print(f"Analyzing state flows in: {doc.metadata['section']} ({chunk_info})")
        
        # Let the graph transformer identify and extract any procedural elements
        graph_docs = state_transformer.convert_to_graph_documents([doc])

        
        # Only add to graph if procedural elements were found
        if graph_docs:

            # Add section node to track processed content
            graph.add_graph_documents(
                graph_docs,
                include_source=True,
            )

            # graph.query("""
            # MERGE (p:Section {name: $name, level: $level})
            # SET p.parent_section = $parent,
            #     p.processed_chunks = CASE 
            #         WHEN p.processed_chunks IS NULL THEN [$chunk_num]
            #         ELSE p.processed_chunks + $chunk_num
            #     END
            # """, 
            # name=doc.metadata['section'],
            # level=doc.metadata['level'],
            # parent=doc.metadata.get('parent_section'),
            # chunk_num=doc.metadata['chunk_index'])
            
            print(f"Found and processed state flows in: {doc.metadata['section']} ({chunk_info})")
        else:
            print(f"No state flows found in: {doc.metadata['section']} ({chunk_info})")
        
    except Exception as e:
        print(f"Error processing {doc.metadata['section']} ({chunk_info})")
        print(f"Error: {str(e)}")

# Process all sections
process_sections(sections)

# Add helper query to get full state flow
def get_state_flow(procedure_name=None):
    query = """
    MATCH path = (start:State)-[r:TRANSITIONS_TO*]->(end:State)
    WHERE start.type = 'INITIAL'
    AND end.type = 'FINAL'
    """
    
    if procedure_name:
        query += f"\nAND start.procedure = '{procedure_name}'"
    
    query += """
    RETURN path,
           [r IN relationships(path) | r.condition] as conditions,
           [r IN relationships(path) | r.trigger] as triggers
    """
    
    return graph.query(query)


def test_llm(llm):
    ai_msg = llm.invoke("What model are you?")
    print(ai_msg)
