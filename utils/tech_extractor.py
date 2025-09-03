"""
Technology Extraction Utilities
Functions to extract technologies and skills from job descriptions
"""

import re

def extract_technologies(job_text):
    """Extract technologies and skills from job description text"""
    
    print(f"DEBUG - Input text: '{job_text[:200]}...'" if len(job_text) > 200 else f"DEBUG - Input text: '{job_text}'")
    tech_keywords = [
        # Programming Languages
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'rust', 'swift', 'kotlin', 'scala', 'r', 'javaee', 'go',
        # Web Technologies
        'html', 'css', 'react', 'angular', 'vue', 'node', 'express.js', 'django', 'flask', 'spring', 'laravel', 'html5', 'css3','handlebars', 'nuxt','jquery','asp.net','bootstrap','blazor','razor','zend',
        'laminas','drupal','twig','sass','scss','graphql',
        # Databases & Data Technologies
        'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'sqlite', 'oracle', 'sql server', 'nosql', 'hadoop', 'spark', 'etl', 'databricks','streamlit'
        # Cloud & DevOps
        'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes', 'jenkins', 'terraform', 'ansible', 'iis', 
        # Data & Analytics
        'pandas', 'numpy', 'tensorflow', 'pytorch', 'scikit-learn', 'tableau', 'power bi', 'excel', 'stata', 
        # Mobile Development
        'android', 'ios', 'react native', 'flutter', 'xamarin',
        # Marketing Tools
        'google analytics', 'facebook ads', 'google ads', 'hubspot', 'salesforce', 'mailchimp', 'hootsuite',
        # Business Tools
        'jira', 'confluence', 'slack', 'trello', 'asana', 'notion', 'linux',
        # Additional tools
        'vba', 'power query', 'ms office', 'microsoft office', 'macros', 'excel macros'
    ]
    job_text_lower = job_text.lower()
    found_technologies = []
    
    for tech in tech_keywords:
        tech_lower = tech.lower()
        
        # Special handling for single-letter technologies (like 'r')
        if len(tech_lower) == 1 and tech_lower == 'r':
            r_patterns = [
                r'\br\s+programming\b', r'\br\s+language\b', r'\br\s+studio\b', r'\brstudio\b',
                r'\br\s+statistical\b', r'\bstatistical\s+r\b', r'\busing\s+r\b', r'\bwith\s+r\b',
                r'\bin\s+r\b', r'\br\s+software\b', r'\br\s+package\b', r'\br\s+script\b',
                r'\br\s+code\b', r'\br\s+analysis\b', r'\bknowledge\s+of\s+r\b',
                r'\bexperience\s+with\s+r\b', r'\bproficient\s+in\s+r\b',
                r'\br\s+and\s+python\b', r'\bpython\s+and\s+r\b', r'\br\s+or\s+python\b',
                r'\bpython\s+or\s+r\b', r'\br\s*[,/]\s*python\b', r'\bpython\s*[,/]\s*r\b'
            ]
            
            if any(re.search(pattern, job_text_lower) for pattern in r_patterns):
                found_technologies.append('R')
        
        # Special handling for Scala programming language
        elif tech_lower == 'scala':
            scala_patterns = [
                r'\bscala\s+programming\b', r'\bscala\s+language\b', r'\bscala\s+developer\b',
                r'\bscala\s+engineer\b', r'\bscala\s+development\b', r'\busing\s+scala\b', r'\bwith\s+scala\b',
                r'\bin\s+scala\b', r'\bscala\s+code\b', r'\bscala\s+application\b', r'\bscala\s+service\b',
                r'\bknowledge\s+of\s+scala\b', r'\bexperience\s+with\s+scala\b', r'\bproficient\s+in\s+scala\b',
                r'\bscala\s+and\s+java\b', r'\bjava\s+and\s+scala\b', r'\bscala\s+or\s+java\b',
                r'\bjava\s+or\s+scala\b', r'\bscala\s*[,/]\s*java\b', r'\bjava\s*[,/]\s*scala\b',
                r'\bscala\s+skills\b', r'\bscala\s+expertise\b', r'\bscala\s+background\b'
            ]
            
            if any(re.search(pattern, job_text_lower) for pattern in scala_patterns):
                found_technologies.append('Scala')
        
        # Special handling for Go programming language
        elif tech_lower == 'go':
            go_patterns = [
                r'\bgo\s+programming\b', r'\bgo\s+language\b', r'\bgo\s+developer\b',
                r'\bgo\s+engineer\b', r'\bgolang\b', r'\busing\s+go\b', r'\bwith\s+go\b',
                r'\bin\s+go\b', r'\bgo\s+code\b', r'\bgo\s+application\b', r'\bgo\s+service\b',
                r'\bknowledge\s+of\s+go\b', r'\bexperience\s+with\s+go\b', r'\bproficient\s+in\s+go\b',
                r'\bgo\s+and\s+python\b', r'\bpython\s+and\s+go\b', r'\bgo\s+or\s+python\b',
                r'\bpython\s+or\s+go\b', r'\bgo\s*[,/]\s*python\b', r'\bpython\s*[,/]\s*go\b'
            ]
            
            if any(re.search(pattern, job_text_lower) for pattern in go_patterns):
                found_technologies.append('Go')
        
        # Special handling for iOS mobile platform
        elif tech_lower == 'ios':
            ios_patterns = [
                r'\bios\s+app\b', r'\bios\s+application\b', r'\bios\s+development\b', r'\bios\s+developer\b',
                r'\bios\s+mobile\b', r'\bios\s+sdk\b', r'\bios\s+platform\b', r'\bios\s+device\b',
                r'\bnative\s+ios\b', r'\bmobile\s+ios\b', r'\bswift\s+ios\b', r'\bios\s+swift\b',
                r'\bios\s+and\s+android\b', r'\bandroid\s+and\s+ios\b', r'\bios\s+or\s+android\b',
                r'\bandroid\s+or\s+ios\b', r'\bios\s*[,/]\s*android\b', r'\bandroid\s*[,/]\s*ios\b',
                r'\bios\s+programming\b', r'\bios\s+engineer\b', r'\busing\s+ios\b', r'\bwith\s+ios\b',
                r'\bknowledge\s+of\s+ios\b', r'\bexperience\s+with\s+ios\b', r'\bproficient\s+in\s+ios\b',
                r'\bios\s+skills\b', r'\bios\s+expertise\b', r'\bxcode\s+ios\b', r'\bios\s+xcode\b'
            ]
            
            if any(re.search(pattern, job_text_lower) for pattern in ios_patterns):
                found_technologies.append('iOS')
        
        # Special handling for Excel
        elif tech_lower == 'excel':
            excel_patterns = [
                r'\bmicrosoft\s+excel\b', r'\bms\s+excel\b', r'\bexcel\s+spreadsheet\b',
                r'\bexcel\s+workbook\b', r'\bexcel\s+formula\b', r'\bexcel\s+macro\b',
                r'\bexcel\s+pivot\b', r'\bexcel\s+chart\b', r'\bexcel\s+data\b',
                r'\bexcel\s+analysis\b', r'\bexcel\s+modeling\b', r'\bexcel\s+reporting\b',
                r'\busing\s+excel\b', r'\bwith\s+excel\b', r'\bin\s+excel\b',
                r'\bknowledge\s+of\s+excel\b', r'\bexperience\s+with\s+excel\b',
                r'\bproficient\s+in\s+excel\b', r'\badvanced\s+excel\b', r'\bbasic\s+excel\b',
                r'\bintermediate\s+excel\b', r'\bexcel\s+skills\b', r'\bexcel\s+expert\b'
            ]
            
            if any(re.search(pattern, job_text_lower) for pattern in excel_patterns):
                found_technologies.append('Excel')
        
        # Regular matching for multi-character technologies
        else:
            pattern_boundary = rf'\b{re.escape(tech_lower)}\b'
            pattern_flexible = re.escape(tech_lower)
            
            if re.search(pattern_boundary, job_text_lower) or re.search(pattern_flexible, job_text_lower):
                # Preserve proper casing for certain technologies
                if tech.upper() in ['SQL', 'HTML', 'CSS', 'API', 'REST', 'JSON', 'XML', 'ETL', 'HTML5', 'CSS3', 'VBA']:
                    found_technologies.append(tech.upper())
                elif tech in ['Node.js', 'MongoDB', 'PostgreSQL', 'MySQL', 'GraphQL', 'JavaScript', 'TypeScript', 'Power BI', 'Power Query']:
                    found_technologies.append(tech)
                else:
                    found_technologies.append(tech.title())
    
    print(f"DEBUG - Technologies found: {found_technologies}")
    
    result = ', '.join(sorted(list(set(found_technologies)))) if found_technologies else None
    print(f"DEBUG - Final result: '{result}'")
    

    return result
