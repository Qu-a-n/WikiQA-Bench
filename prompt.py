class WikiQA:

    # benchmark
    def prompt_for_bsl(self, question: str, table: str) -> str:
        template = """You are an expert in handling table Q&A questions. You will receive a table and a question. Please analyse the table and give the answer(s) to the question.
Keep your answer brief and concise. Avoid repeating words from the question.

Here is an example to illustrate how to answer concisely:
- Question: What is the average number of tropical cyclones per season?
Good Answer: "10.6"
Bad Answer: "Average number of tropical cyclones per season: 10.6"
         
Format your response as the following json template:
```json
{{
    "question": {question},
    "table": {table},
    "thought_process": "<Describe your thought process and steps you took to get the answer(s)>",
    "answer": "Answer1, Answer2, ... <Fill in the answer(s) you get after analyzing the table>"
}}
```

Here are some examples:
Example 1:
```json
{{
    "question": "what was the last year where this team was a part of the usl a-league?",
    "table": 
'''
Year  Division              League Regular Season        Playoffs        Open Cup Avg. Attendance
 2001         2        USL A-League   4th, Western   Quarterfinals Did not qualify           7,169
 2002         2        USL A-League   2nd, Pacific       1st Round Did not qualify           6,260
 2003         2        USL A-League   3rd, Pacific Did not qualify Did not qualify           5,871
 2004         2        USL A-League   1st, Western   Quarterfinals       4th Round           5,628
 2005         2  USL First Division            5th   Quarterfinals       4th Round           6,028
 2006         2  USL First Division           11th Did not qualify       3rd Round           5,575
 2007         2  USL First Division            2nd      Semifinals       2nd Round           6,851
 2008         2  USL First Division           11th Did not qualify       1st Round           8,567
 2009         2  USL First Division            1st      Semifinals       3rd Round           9,734
 2010         2 USSF D-2 Pro League 3rd, USL (3rd)   Quarterfinals       3rd Round          10,727
''',
    "thought_process": '''First we need to identify relevant rows: rows in the table where the "Division" column contains 'USL A-League'. Then we need to extract the corresponding "Year" values from the identified rows. After collecting the years where the team was in the USL A-League, we will find the maximum year, which will represent the last year they were in that league. 
Let's analyze the provided data row by row:
2001: USL A-League
2002: USL A-League
2003: USL A-League
2004: USL A-League
2005: USL First Division (not relevant)
2006: USL First Division (not relevant)
2007: USL First Division (not relevant)
2008: USL First Division (not relevant)
2009: USL First Division (not relevant)
2010: USSF D-2 Pro League (not relevant)
From the rows, the years where the team was in the "USL A-League" are: 2004
''',
    "answer": "2004"
}}
```
"""
        prompt = template.format(question=question, table=table)
        return prompt
    
