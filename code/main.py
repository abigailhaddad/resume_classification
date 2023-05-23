# -*- coding: utf-8 -*-
"""
Created on Sat May 20 20:55:57 2023

@author: abiga
"""
import generate_resumes
import gpt_prompt_software
import model_evaluation_formal


def make_prompt_dict():
    """Return the dict with prompts."""
    return {"prompt1": "please respond YES if this candidate has worked in a role where they have been coding in R or Python to solve data science tasks and NO if they have not or if you are not sure.",
                 "prompt2": "please respond YES if this candidate lists specific data science languages and libraries using R or Python and describes how they are using them on the job and NO if they don't or you're not sure",
                 "prompt3": "I'm evaluating this resume for a mid-level data science role and I'm looking for evidence that the candidate can immediately start building tools in R or Python to meet business needs, and both understand the technology and work with stakeholders to communicate. Please return YES if the resume has those skills and NO if it doesn't or you're not sure",
                 "prompt4": "please respond YES if there is direct evidence in the form of specific descriptions of tasks for how the candidate is themselves writing R or Python code to solve on the job data science problems. Just listing a tool is not sufficient evidence -- we're looking for specific descriptions showing they are coding in these tools to solve data science problems --- beyond business reporting/dashboarding, and not just in a supervisory context, and not just while using proprietary statistical software packages like SPSS, SAS, Stata, or MATLAB. please return YES if you see substantial evidence of this and NO if you don't or you're not sure",
                 "summary": "please briefly summarize the data science background of the candidate. ignore list of tools -- focus instead on descriptions the candidate gives of specific ways they are using tools",
                 "named_entity": "please return a list of the programming language and software tools listed in this resume in conjunction with speciific tasks the candidate describes"}



input_generate_resumes="resume_data_prompts"
output_pull_data_from_docs="fake resumes"
output_gpt_prompt_software="new_fake_data_sci_coded"
output_model_evaluation_formal="new_crosstab_fake"
prompt_dict= make_prompt_dict()

generate_resumes.main(input_generate_resumes, output_pull_data_from_docs)
gpt_prompt_software.main(output_pull_data_from_docs, output_gpt_prompt_software, prompt_dict)
model_evaluation_formal.main(output_gpt_prompt_software, output_model_evaluation_formal, prompt_dict)


    