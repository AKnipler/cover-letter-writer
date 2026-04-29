import regex as re
import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from docx import Document
from python_docx_replace import docx_replace
import time
from datetime import datetime
from docx2pdf import convert
from src import functions as fn





if __name__ == "__main__":
    
    # Time the program
    start_time = time.time()

    # Load environment variables from .env file (e.g. OpenAI API key)
    load_dotenv()



    #       ****        GET JOB LISTING     ****
    URL = ""
    while not URL:
        URL = input("Enter the URL of the website to scrape: ")
    
    content = fn.send_request(URL)
    
    (job_listing, advertiser_name, position_title) = fn.page_extraction(content)

    print(f"Job Listing: \n{job_listing}\n")
    print(f"Advertiser Name: {advertiser_name}, Job Title: {position_title}")

    # Load candidate profile and workflow instructions from input files
    with open('inputs/Candidate Profile.txt', 'r', encoding="utf-8") as f:
        # Safely evaluate the string as a Python literal
        candidate_profile = f.read()

    with open('inputs/Workflow.json', 'r', encoding="utf-8") as f:
        # Safely evaluate the string as a Python literal
        workflow = json.load(f)




    #       ****        RUN WORKFLOW        ****
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    for step in workflow:

        print(f"********** Step: {step} **********")
        if step == "1":
            msg = workflow[step] + "Job Listing: \n" + job_listing
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": msg}
                ]
            )
            S1_output = response.choices[0].message.content
            print(f"Step 1 Output: {S1_output}\n")

        elif step == "2":
            msg = workflow[step] + "Job Listing Analysis: \n" + S1_output + "\nCandidate Information: \n" + candidate_profile
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": msg}
                ]
            )
            S2_output = response.choices[0].message.content 
            print(f"Step 2 Output: {S2_output}\n")

        elif step == "3":
            msg = workflow[step] + "Job Listing Analysis: \n" + S1_output + "\nCandidate Fit Insights: \n" + S2_output + "\nCandidate Information: \n" + candidate_profile + "\n\nWrite the cover letter."
            response = client.chat.completions.create(
                model="gpt-5.1", # More expensive model for the cover letter generation: prioritise quality here
                messages=[
                    {"role": "user", "content": msg}
                ]
            )
            S3_output = response.choices[0].message.content
            print(f"Step 3 Output: {S3_output}\n")

    replacements = {
        "[POSITION TITLE]": position_title,
        "[COVER LETTER BODY]": S3_output,
        "[DATE]": "NA" # Date has to be done manually in the template for formatting reasons
    }
    



    #       ****    MAKE DOCUMENT WITH CONTENT  ****

    # copy template to new file and replace placeholders with generated content
    formatted_advertiser_name = re.sub(r' +',' ', advertiser_name)
    formatted_advertiser_name = re.sub(r'[^a-zA-Z0-9_]', '', formatted_advertiser_name).replace(" ", "_").lower()
    cover_letter_template_path = 'inputs/template_cover_letter.docx'
    file_name = str(datetime.now().strftime("%Y%m%d_"))+ formatted_advertiser_name + "_cover_letter_ash_knipler.docx"
    output_cover_letter_path = 'output/' + file_name
    fn.create_cover_letter(cover_letter_template_path, output_cover_letter_path, replacements)

    # make pdf version of the cover letter
    if os.path.exists(output_cover_letter_path.replace(".docx", ".pdf")):
        print("PDF already exists, skipping conversion.")
    else:
        fn.convert(output_cover_letter_path, output_cover_letter_path.replace(".docx", ".pdf"))




    #       ****        PROGRAM COMPLETE        ****
    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.2f} seconds")