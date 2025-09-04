"""
Job Categorization Utilities
Functions to categorize job titles into Philippine IT Market categories
"""

def categorize_job_title(job_title):
    """
    Categorize job title based on the 11 Philippine IT Market Analysis categories
    Returns category name or 'Excluded - Non IT' if no match found
    """
    title_lower = job_title.lower().strip()
    title_clean = title_lower.replace('|', '').replace('-', ' ')
    
    # 1. DevOps and Platform Engineering
    devops_keywords = [
        'devops', 'platform engineer', 'site reliability', 'sre', 
        'infrastructure engineer', 'terraform', 'kubernetes', 'docker',
        'ci/cd', 'pipeline', 'release engineer',
        'infrastructure automation', 'deployment engineer', 'platform architect'
    ]
    
    # 2. Quality Assurance and Testing  
    qa_keywords = [
        'qa engineer', 'quality assurance', 'test', 'tester',
        'qa analyst', 'testing', 'automation tester', 'test planning',
        'functional test', 'tester', 'quality',
        'test automation', 'qa specialist', 'qa automation', 'qa' 
    ]
    
    # 3. Database Administration
    db_keywords = [
        'database administrator', 'dba', 'database',
        'sql administrator', 'metadata', "db administrator","sql server","migration",'extract transform','data architect','data administrator'
    ]
    
    # 4. Cloud Computing
    cloud_keywords = [
        'cloud', 'cloud specialist', 'aws', 'azure', 'gcp', 'solutions architect'
    ]
    
    # 5. Cybersecurity
    security_keywords = [
        'security', 'security officer', 'cybersecurity', 'penetration', 
        'application security', 'infosec', 'cyber security', 'cyber', 'it security'
    ]
    
    # 6. Data Science and Analysis
    data_keywords = [
        'data scientist', 'data analyst', 'data eng', 'business intelligence',
        'machine learning', 'analytics', 'bi analyst', 'reporting analyst', 'data conversion',
        'ml', 'web analyst','sql','data visualization','analyst','data annotator','data specialist','powerbi','data workflow analyst',
        'data strategy','sql analyst', 'sql', 'bi reporting', 
    ]
    
    # 7. Software, Web, and Mobile Development (COMBINED CATEGORY)
    software_web_mobile_keywords = [
        # Web Development
        'web developer', 'frontend developer', 'backend developer',
        'full stack', 'fullstack', 'angular developer', 'react developer',
        'vue', 'nodejs', 'web engineer', 'wordpress', 'ui developer', 
        'web designer', 'frontend engineer', 'ui/ux developer',
        'javascript developer', 'html', 'css developer', 'java enterprise','java','ui/ux','ui','ux','next.js',
        # Mobile Development
        'mobile developer', 'android developer', 
        'app developer', 'android', 'mobile app', 'cobol',
        # Software Development
        'software developer', 'software engineer', 'programmer',
        'application developer',
        'java developer', 'python developer', 'golang developer',
        'developer', 'engineer', '.net developer', 'php developer',
        'c++ developer', 'technical developer', 'kong developer',
        'backend engineer', 'application engineer', 'systems developer', 
        'solutions engineer', 'solutions', 'product designer','building tool', 'website', 'website administrator',
        'software development','software architect','ai & automation','ai architect','nodejs'
    ]
    
    # 8. Network and Systems Administration  
    sysadmin_keywords = [
        'system administrator', 'systems administrator', 'sysadmin',
        'network administrator', 'it administrator', 'server administrator',
        'system analyst', 'it officer', 'system i', 'infrastructure specialist',
        'systems engineer', 'network engineer', 'server engineer', 'ip telephony', 'telephony', 'system','technology architecture'
    ]
    
    # 9. Business and Systems Analysis
    business_keywords = [
        'business analyst', 'systems analyst', 'functional analyst',
        'process analyst', 'business systems analyst',
        'requirements analyst', 'system analyst', 'functional',
        'business systems', 'process improvement', 'presales', 'payroll','sap','enterprise','sap consultant','sap fico', 'sap associate',
        'sap administrator', 'technical consultant', 
    ]
    
    # 10. IT Management and Operations
    it_management_keywords = [
        'it project manager', 'project manager', 'owner',
        'it strategic business partner', 'business partner manager',
        'billing consultant', 'technical project manager',
        'business development', 
        'manager', 'project management', 'itsm', 'director', 'governance', 'compliance', 'management', 'it operations','it project coordinator','chief technology officer',
        'it supervisor','chief transformation officer', 'it project lead', 'it project', 'it lead', 'project administrator','it specialist','scrum', 'enterprise solutions', 
    ]
    
    # 11. IT Support and Helpdesk
    support_keywords = [
        'it support', 'technical support', 'help desk', 'desktop support',
        'support', 'support analyst', 'it technician',
        'computer technician', 'user productivity', 'end user', 
        'contact center', 'field support',
        'helpdesk', 'technical', 'support lead', 'deskside support', 'it staff', 'it service', 'it desk','service desk','computer operator','assistant', 
        'information technology','information staff','technology staff', "it intern", 'it specialist'
    ]

    
    # Check categories in order of specificity

    if any(keyword in title_clean for keyword in devops_keywords):
        return 'DevOps and Platform Engineering'
    
    if any(keyword in title_clean for keyword in qa_keywords):
        return 'Quality Assurance and Testing'
    
    if any(keyword in title_clean for keyword in db_keywords):
        return 'Database Administration'
    
    if any(keyword in title_clean for keyword in business_keywords):
        return 'Business and Systems Analysis'
    
    if any(keyword in title_clean for keyword in cloud_keywords):
        return 'Cloud Computing'
    
    if any(keyword in title_clean for keyword in security_keywords):
        return 'Cybersecurity'
    
    if any(keyword in title_clean for keyword in support_keywords):
        return 'IT Support and Helpdesk'

    if any(keyword in title_clean for keyword in data_keywords):
        return 'Data Science and Analysis'
    
    if any(keyword in title_clean for keyword in software_web_mobile_keywords):
        return 'Software, Web, and Mobile Development'
    
    if any(keyword in title_clean for keyword in sysadmin_keywords):
        return 'Network and Systems Administration'
    
    if any(keyword in title_clean for keyword in it_management_keywords):
        return 'IT Management and Operations'
    
    # If no match found, still consider it IT-related since it passed the non-IT filter
    return 'Other IT'






