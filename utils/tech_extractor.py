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
        'html', 'css', 'react', 'angular', 'vue', 'node', 'express', 'django', 'flask', 'spring', 'laravel', 'html5', 'css3','handlebars', 'nuxt','jquery','asp.net','bootstrap','blazor','razor','zend',
        'laminas','drupal','twig','sass','scss','graphql',
        # Databases & Data Technologies
        'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'sqlite', 'oracle', 'sql server', 'nosql', 'hadoop', 'spark', 'databricks',
        # ETL/Data Pipeline Tools
        'airflow', 'apache airflow', 'dbt', 'fivetran', 'stitch', 'talend', 'informatica', 'pentaho', 'ssis', 'alteryx',
        'aws glue', 'azure data factory', 'google dataflow', 'kafka', 'apache kafka', 'apache flink', 'kinesis',
        # AI/ML Technologies
        'langchain', 'langgraph', 'graphrag', 'llamaindex', 'hugging face', 'openai api', 'pinecone', 'mlflow', 'wandb',
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
        'red hat', 'rhel', 'ubuntu', 'centos', 'debian', 'powershell', 'bash', 'zsh', 'sap',
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
        
        elif tech_lower == 'sap':
            # Don't match if it's part of ASAP
            if not re.search(r'\basap\b', job_text_lower):
                sap_patterns = [
                    r'\bsap\s+erp\b', r'\bsap\s+hana\b', r'\bsap\s+abap\b', r'\bsap\s+basis\b',
                    r'\bsap\s+consultant\b', r'\bsap\s+developer\b', r'\bsap\s+analyst\b',
                    r'\bsap\s+modules\b', r'\bsap\s+system\b', r'\bsap\s+implementation\b',
                    r'\bsap\s+configuration\b', r'\bsap\s+migration\b', r'\bsap\s+integration\b',
                    r'\bsap\s+s/4hana\b', r'\bsap\s+successfactors\b', r'\bsap\s+ariba\b',
                    r'\bsap\s+concur\b', r'\bsap\s+fieldglass\b', r'\bsap\s+hybris\b',
                    r'\bsap\s+application\b', r'\bsap\s+applications\b', r'\bsap\s+fico\b',
                    r'\busing\s+sap\b', r'\bwith\s+sap\b', r'\bsap\s+experience\b',
                    r'\bknowledge\s+of\s+sap\b', r'\bexperience\s+with\s+sap\b', r'\bproficient\s+in\s+sap\b',
                    r'\bsap\s+skills\b', r'\bsap\s+expertise\b', r'\bsap\s+functional\b',
                    r'\bsap\s+technical\b', r'\bsap\s+finance\b', r'\bsap\s+hr\b'
                ]
                
                if any(re.search(pattern, job_text_lower) for pattern in sap_patterns):
                    found_technologies.append('SAP')
        
        # Special handling for AWS cloud platform
        elif tech_lower == 'aws':
            aws_patterns = [
                r'\baws\s+cloud\b', r'\baws\s+services\b', r'\baws\s+platform\b', r'\baws\s+infrastructure\b',
                r'\baws\s+certification\b', r'\baws\s+certified\b', r'\baws\s+architect\b', r'\baws\s+engineer\b',
                r'\baws\s+developer\b', r'\baws\s+devops\b', r'\baws\s+solutions\b', r'\baws\s+experience\b',
                r'\busing\s+aws\b', r'\bwith\s+aws\b', r'\bdeploy\s+to\s+aws\b', r'\bmigrate\s+to\s+aws\b',
                r'\baws\s+and\s+azure\b', r'\bazure\s+and\s+aws\b', r'\baws\s+or\s+azure\b',
                r'\bazure\s+or\s+aws\b', r'\baws\s*[,/]\s*azure\b', r'\bazure\s*[,/]\s*aws\b',
                r'\baws\s+lambda\b', r'\baws\s+s3\b', r'\baws\s+ec2\b', r'\baws\s+rds\b',
                r'\bknowledge\s+of\s+aws\b', r'\bexperience\s+with\s+aws\b', r'\bproficient\s+in\s+aws\b',
                r'\baws\s+skills\b', r'\baws\s+expertise\b', r'\baws\s+background\b'
            ]
            
            if any(re.search(pattern, job_text_lower) for pattern in aws_patterns):
                found_technologies.append('AWS')
        
        
        # Special handling for SSIS (SQL Server Integration Services)
        elif tech_lower == 'ssis':
            ssis_patterns = [
                r'\bssis\s+package\b', r'\bssis\s+development\b', r'\bssis\s+developer\b',
                r'\bssis\s+integration\b', r'\bssis\s+etl\b', r'\betl\s+ssis\b',
                r'\bsql\s+server\s+integration\s+services\b', r'\bssis\s+experience\b',
                r'\busing\s+ssis\b', r'\bwith\s+ssis\b', r'\bssis\s+and\s+sql\b',
                r'\bsql\s+and\s+ssis\b', r'\bssis\s+or\s+talend\b', r'\btalend\s+or\s+ssis\b',
                r'\bssis\s*[,/]\s*sql\b', r'\bsql\s*[,/]\s*ssis\b',
                r'\bknowledge\s+of\s+ssis\b', r'\bexperience\s+with\s+ssis\b', r'\bproficient\s+in\s+ssis\b',
                r'\bssis\s+skills\b', r'\bssis\s+expertise\b', r'\bmicrosoft\s+ssis\b'
            ]
            
            if any(re.search(pattern, job_text_lower) for pattern in ssis_patterns):
                found_technologies.append('SSIS')
        
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

           
        # Special handling for PHP programming language (avoid peso references)
        elif tech_lower == 'php':
            # First check if it's a peso reference (PHP followed by numbers)
            peso_patterns = [
                r'\bphp\s*\d', r'\bphp\s*[0-9,k]+\b', r'\bphp\s*\d+[,.]?\d*[km]?\b',
                r'\bsalary.*php\b', r'\bcompensation.*php\b', r'\bbudget.*php\b',
                r'\bcost.*php\b', r'\bworth.*php\b', r'\ballowance.*php\b'
            ]
            
            # Don't match if it's clearly about pesos
            is_peso_context = any(re.search(pattern, job_text_lower) for pattern in peso_patterns)
            
            if not is_peso_context:
                php_patterns = [
                    r'\bphp\s+developer\b', r'\bphp\s+programming\b', r'\bphp\s+development\b',
                    r'\bphp\s+engineer\b', r'\bphp\s+web\b', r'\bweb\s+php\b',
                    r'\bphp\s+and\s+mysql\b', r'\bmysql\s+and\s+php\b', r'\bphp\s+mysql\b',
                    r'\bphp\s+framework\b', r'\blaravel\s+php\b', r'\bphp\s+laravel\b',
                    r'\bphp\s*[,/]\s*javascript\b', r'\bjavascript\s*[,/]\s*php\b',
                    r'\bphp\s*[,/]\s*html\b', r'\bhtml\s*[,/]\s*php\b',
                    r'\busing\s+php\b', r'\bwith\s+php\b', r'\bbackend\s+php\b',
                    r'\bknowledge\s+of\s+php\b', r'\bexperience\s+with\s+php\b', r'\bproficient\s+in\s+php\b',
                    r'\bphp\s+skills\b', r'\bphp\s+expertise\b', r'\bphp\s+application\b',
                    r'\bphp\s+code\b', r'\bphp\s+script\b', r'\bphp\s+backend\b'
                ]
                
                if any(re.search(pattern, job_text_lower) for pattern in php_patterns):
                    found_technologies.append('PHP')
        
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
