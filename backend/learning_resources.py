"""Curated learning resources catalogue for career-path skill gaps (ported from CareerCopilot)."""

LEARNING_RESOURCES = {
    # --- Data & Analytics ---
    "Tableau": [
        {"title": "Tableau Fundamentals", "provider": "Tableau Learning", "duration_hours": 20, "cost": "Free", "level": "beginner", "url": "https://www.tableau.com/learn/training", "type": "video_course"},
        {"title": "Tableau for Data Science", "provider": "Udemy", "duration_hours": 10, "cost": "$15", "level": "intermediate", "url": "https://www.udemy.com/course/tableau10/", "type": "video_course"},
    ],
    "Python": [
        {"title": "Python for Everybody", "provider": "Coursera", "duration_hours": 40, "cost": "Free (audit)", "level": "beginner", "url": "https://www.coursera.org/specializations/python", "type": "video_course"},
        {"title": "Automate the Boring Stuff with Python", "provider": "Al Sweigart", "duration_hours": 30, "cost": "Free", "level": "beginner", "url": "https://automatetheboringstuff.com/", "type": "book"},
        {"title": "Python Data Science Handbook", "provider": "Jake VanderPlas", "duration_hours": 25, "cost": "Free", "level": "intermediate", "url": "https://jakevdp.github.io/PythonDataScienceHandbook/", "type": "book"},
    ],
    "SQL": [
        {"title": "Intro to SQL", "provider": "Khan Academy", "duration_hours": 15, "cost": "Free", "level": "beginner", "url": "https://www.khanacademy.org/computing/computer-programming/sql", "type": "interactive"},
        {"title": "SQL for Data Analysis", "provider": "Mode Analytics", "duration_hours": 12, "cost": "Free", "level": "intermediate", "url": "https://mode.com/sql-tutorial/", "type": "interactive"},
    ],
    "R": [
        {"title": "R Programming", "provider": "Coursera", "duration_hours": 30, "cost": "Free (audit)", "level": "beginner", "url": "https://www.coursera.org/learn/r-programming", "type": "video_course"},
    ],
    "Power BI": [
        {"title": "Power BI Guided Learning", "provider": "Microsoft", "duration_hours": 25, "cost": "Free", "level": "beginner", "url": "https://learn.microsoft.com/en-us/power-bi/", "type": "interactive"},
    ],
    "Statistical Analysis": [
        {"title": "Statistics and Probability", "provider": "Khan Academy", "duration_hours": 30, "cost": "Free", "level": "beginner", "url": "https://www.khanacademy.org/math/statistics-probability", "type": "interactive"},
        {"title": "Statistics with R", "provider": "Coursera", "duration_hours": 20, "cost": "Free (audit)", "level": "intermediate", "url": "https://www.coursera.org/specializations/statistics", "type": "video_course"},
    ],
    "Data Visualization": [
        {"title": "Data Visualization with Python", "provider": "Coursera", "duration_hours": 18, "cost": "Free (audit)", "level": "intermediate", "url": "https://www.coursera.org/learn/python-for-data-visualization", "type": "video_course"},
    ],
    "Excel": [
        {"title": "Excel Skills for Business", "provider": "Coursera", "duration_hours": 30, "cost": "Free (audit)", "level": "intermediate", "url": "https://www.coursera.org/specializations/excel", "type": "video_course"},
        {"title": "Excel Formulas & Functions", "provider": "Microsoft", "duration_hours": 10, "cost": "Free", "level": "beginner", "url": "https://support.microsoft.com/en-us/excel", "type": "interactive"},
    ],
    "Advanced Data Analytics": [
        {"title": "Google Advanced Data Analytics Certificate", "provider": "Coursera", "duration_hours": 80, "cost": "Free (audit)", "level": "intermediate", "url": "https://www.coursera.org/professional-certificates/google-advanced-data-analytics", "type": "certificate"},
    ],
    # --- AI & Machine Learning ---
    "Machine Learning": [
        {"title": "Machine Learning", "provider": "Coursera (Andrew Ng)", "duration_hours": 60, "cost": "Free (audit)", "level": "intermediate", "url": "https://www.coursera.org/learn/machine-learning", "type": "video_course"},
        {"title": "fast.ai Practical Deep Learning", "provider": "fast.ai", "duration_hours": 40, "cost": "Free", "level": "intermediate", "url": "https://course.fast.ai/", "type": "video_course"},
    ],
    "Deep Learning": [
        {"title": "Deep Learning Specialization", "provider": "Coursera (Andrew Ng)", "duration_hours": 80, "cost": "Free (audit)", "level": "advanced", "url": "https://www.coursera.org/specializations/deep-learning", "type": "video_course"},
    ],
    "TensorFlow": [
        {"title": "TensorFlow Developer Certificate", "provider": "Coursera", "duration_hours": 60, "cost": "Free (audit)", "level": "intermediate", "url": "https://www.coursera.org/professional-certificates/tensorflow-in-practice", "type": "certificate"},
    ],
    "NLP": [
        {"title": "Natural Language Processing Specialization", "provider": "Coursera", "duration_hours": 50, "cost": "Free (audit)", "level": "advanced", "url": "https://www.coursera.org/specializations/natural-language-processing", "type": "video_course"},
    ],
    # --- Product & Management ---
    "Product Management": [
        {"title": "Product Management Fundamentals", "provider": "Product School", "duration_hours": 20, "cost": "Free", "level": "beginner", "url": "https://productschool.com/free-product-management-resources", "type": "video_course"},
        {"title": "Digital Product Management", "provider": "Coursera", "duration_hours": 15, "cost": "Free (audit)", "level": "intermediate", "url": "https://www.coursera.org/learn/uva-darden-digital-product-management", "type": "video_course"},
    ],
    "Product Lifecycle Management": [
        {"title": "Product Lifecycle Management Essentials", "provider": "LinkedIn Learning", "duration_hours": 8, "cost": "Free trial", "level": "intermediate", "url": "https://www.linkedin.com/learning/", "type": "video_course"},
    ],
    "Go-to-Market Strategies": [
        {"title": "Go-to-Market Strategy", "provider": "HubSpot Academy", "duration_hours": 6, "cost": "Free", "level": "intermediate", "url": "https://academy.hubspot.com/", "type": "video_course"},
    ],
    "Agile": [
        {"title": "Agile with Atlassian Jira", "provider": "Coursera", "duration_hours": 15, "cost": "Free (audit)", "level": "beginner", "url": "https://www.coursera.org/learn/agile-atlassian-jira", "type": "video_course"},
    ],
    "Project Management": [
        {"title": "Google Project Management Certificate", "provider": "Coursera", "duration_hours": 120, "cost": "$49/month", "level": "beginner", "url": "https://www.coursera.org/professional-certificates/google-project-management", "type": "certificate"},
        {"title": "Introduction to Project Management", "provider": "Coursera", "duration_hours": 18, "cost": "Free (audit)", "level": "beginner", "url": "https://www.coursera.org/learn/project-management-foundations", "type": "video_course"},
    ],
    "Scrum": [
        {"title": "Scrum Master Certification Prep", "provider": "Scrum.org", "duration_hours": 15, "cost": "Free", "level": "beginner", "url": "https://www.scrum.org/resources/scrum-guide", "type": "reading"},
    ],
    # --- Business & Finance ---
    "Financial Modeling": [
        {"title": "Financial Modeling Fundamentals", "provider": "Corporate Finance Institute", "duration_hours": 25, "cost": "Free", "level": "intermediate", "url": "https://corporatefinanceinstitute.com/resources/", "type": "video_course"},
    ],
    "Financial Analysis": [
        {"title": "Financial Analysis and Decision Making", "provider": "edX", "duration_hours": 30, "cost": "Free (audit)", "level": "intermediate", "url": "https://www.edx.org/learn/financial-analysis", "type": "video_course"},
    ],
    "Budgeting & Forecasting": [
        {"title": "Budgeting and Forecasting", "provider": "LinkedIn Learning", "duration_hours": 8, "cost": "Free trial", "level": "intermediate", "url": "https://www.linkedin.com/learning/", "type": "video_course"},
    ],
    "Accounting (GAAP/IFRS)": [
        {"title": "Introduction to Financial Accounting", "provider": "Coursera", "duration_hours": 25, "cost": "Free (audit)", "level": "beginner", "url": "https://www.coursera.org/learn/wharton-accounting", "type": "video_course"},
    ],
    "Business Analysis": [
        {"title": "Business Analysis Foundations", "provider": "LinkedIn Learning", "duration_hours": 10, "cost": "Free trial", "level": "beginner", "url": "https://www.linkedin.com/learning/", "type": "video_course"},
        {"title": "IIBA ECBA Study Guide", "provider": "IIBA", "duration_hours": 40, "cost": "Free", "level": "intermediate", "url": "https://www.iiba.org/business-analysis-certifications/ecba/", "type": "reading"},
    ],
    # --- Marketing ---
    "Digital Marketing": [
        {"title": "Google Digital Marketing Certificate", "provider": "Coursera", "duration_hours": 80, "cost": "Free (audit)", "level": "beginner", "url": "https://www.coursera.org/professional-certificates/google-digital-marketing-ecommerce", "type": "certificate"},
        {"title": "Digital Marketing Course", "provider": "HubSpot Academy", "duration_hours": 12, "cost": "Free", "level": "beginner", "url": "https://academy.hubspot.com/courses/digital-marketing", "type": "video_course"},
    ],
    "SEO/SEM": [
        {"title": "SEO Training Course", "provider": "HubSpot Academy", "duration_hours": 6, "cost": "Free", "level": "beginner", "url": "https://academy.hubspot.com/courses/seo-training", "type": "video_course"},
        {"title": "Google Ads Certification", "provider": "Google", "duration_hours": 15, "cost": "Free", "level": "intermediate", "url": "https://skillshop.withgoogle.com/", "type": "certificate"},
    ],
    "Content Marketing": [
        {"title": "Content Marketing Certification", "provider": "HubSpot Academy", "duration_hours": 8, "cost": "Free", "level": "beginner", "url": "https://academy.hubspot.com/courses/content-marketing", "type": "video_course"},
    ],
    "Google Analytics": [
        {"title": "Google Analytics Certification", "provider": "Google", "duration_hours": 15, "cost": "Free", "level": "intermediate", "url": "https://skillshop.withgoogle.com/", "type": "certificate"},
    ],
    # --- Technical / Engineering ---
    "JavaScript": [
        {"title": "JavaScript Algorithms & Data Structures", "provider": "freeCodeCamp", "duration_hours": 50, "cost": "Free", "level": "beginner", "url": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/", "type": "interactive"},
        {"title": "The Odin Project - JavaScript", "provider": "The Odin Project", "duration_hours": 80, "cost": "Free", "level": "beginner", "url": "https://www.theodinproject.com/paths/full-stack-javascript", "type": "interactive"},
    ],
    "TypeScript": [
        {"title": "TypeScript Handbook", "provider": "Microsoft", "duration_hours": 15, "cost": "Free", "level": "intermediate", "url": "https://www.typescriptlang.org/docs/handbook/", "type": "reading"},
    ],
    "React": [
        {"title": "React Official Tutorial", "provider": "React.dev", "duration_hours": 20, "cost": "Free", "level": "beginner", "url": "https://react.dev/learn", "type": "interactive"},
    ],
    "Node.js": [
        {"title": "Node.js Tutorial", "provider": "freeCodeCamp", "duration_hours": 30, "cost": "Free", "level": "beginner", "url": "https://www.freecodecamp.org/learn/back-end-development-and-apis/", "type": "interactive"},
    ],
    "AWS": [
        {"title": "AWS Cloud Practitioner Essentials", "provider": "AWS", "duration_hours": 30, "cost": "Free", "level": "beginner", "url": "https://aws.amazon.com/training/", "type": "video_course"},
        {"title": "AWS Solutions Architect - Associate", "provider": "AWS", "duration_hours": 60, "cost": "Free", "level": "intermediate", "url": "https://aws.amazon.com/certification/certified-solutions-architect-associate/", "type": "certificate"},
    ],
    "Azure": [
        {"title": "Azure Fundamentals (AZ-900)", "provider": "Microsoft Learn", "duration_hours": 20, "cost": "Free", "level": "beginner", "url": "https://learn.microsoft.com/en-us/certifications/azure-fundamentals/", "type": "interactive"},
    ],
    "Docker": [
        {"title": "Docker Getting Started", "provider": "Docker", "duration_hours": 10, "cost": "Free", "level": "beginner", "url": "https://docs.docker.com/get-started/", "type": "interactive"},
    ],
    "Kubernetes": [
        {"title": "Kubernetes Basics", "provider": "Kubernetes.io", "duration_hours": 15, "cost": "Free", "level": "intermediate", "url": "https://kubernetes.io/docs/tutorials/kubernetes-basics/", "type": "interactive"},
    ],
    "Git/GitHub": [
        {"title": "Git & GitHub Crash Course", "provider": "freeCodeCamp", "duration_hours": 5, "cost": "Free", "level": "beginner", "url": "https://www.freecodecamp.org/news/git-and-github-crash-course/", "type": "video_course"},
    ],
    # --- Design ---
    "UI/UX Design": [
        {"title": "Google UX Design Certificate", "provider": "Coursera", "duration_hours": 100, "cost": "Free (audit)", "level": "beginner", "url": "https://www.coursera.org/professional-certificates/google-ux-design", "type": "certificate"},
    ],
    "Figma": [
        {"title": "Figma for Beginners", "provider": "Figma", "duration_hours": 10, "cost": "Free", "level": "beginner", "url": "https://help.figma.com/hc/en-us/categories/360002051613", "type": "interactive"},
    ],
    # --- Soft Skills & Leadership ---
    "Communication": [
        {"title": "Improving Communication Skills", "provider": "Coursera", "duration_hours": 12, "cost": "Free (audit)", "level": "beginner", "url": "https://www.coursera.org/learn/wharton-communication", "type": "video_course"},
    ],
    "Leadership": [
        {"title": "Foundations of Leadership", "provider": "edX", "duration_hours": 20, "cost": "Free (audit)", "level": "intermediate", "url": "https://www.edx.org/learn/leadership", "type": "video_course"},
    ],
    "Public Speaking": [
        {"title": "Introduction to Public Speaking", "provider": "Coursera", "duration_hours": 15, "cost": "Free (audit)", "level": "beginner", "url": "https://www.coursera.org/learn/public-speaking", "type": "video_course"},
    ],
    "Negotiation": [
        {"title": "Successful Negotiation", "provider": "Coursera", "duration_hours": 12, "cost": "Free (audit)", "level": "intermediate", "url": "https://www.coursera.org/learn/negotiation-skills", "type": "video_course"},
    ],
    # --- Healthcare ---
    "Medical Terminology": [
        {"title": "Medical Terminology Course", "provider": "Coursera", "duration_hours": 20, "cost": "Free (audit)", "level": "beginner", "url": "https://www.coursera.org/learn/medical-terminology", "type": "video_course"},
    ],
    # --- Cybersecurity ---
    "Cybersecurity": [
        {"title": "Google Cybersecurity Certificate", "provider": "Coursera", "duration_hours": 100, "cost": "Free (audit)", "level": "beginner", "url": "https://www.coursera.org/professional-certificates/google-cybersecurity", "type": "certificate"},
    ],
    # --- Supply Chain ---
    "Supply Chain Management": [
        {"title": "Supply Chain Management Specialization", "provider": "Coursera", "duration_hours": 50, "cost": "Free (audit)", "level": "intermediate", "url": "https://www.coursera.org/specializations/supply-chain-management", "type": "video_course"},
    ],
}
