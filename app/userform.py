from flask import request, session
import re
import phonenumbers


class UserForm(object):
    def __init__(self) -> None:
        self.errors = []
        self.resume_data = {}


    def from_session(self, session_key):
        if session_key in session:
            self.resume_data = session[session_key]


    def from_request(self):
        self.resume_data["name"] = request.form.get("name", "").strip()
        self.resume_data["role_job_name"] = request.form.get("role-job-name", "").strip()
        self.resume_data["email"] = request.form.get("email", "").strip()
        self.resume_data["phone"] = request.form.get("phone", "").strip()
        self.resume_data["address"] = request.form.get("cur-per-address", "").strip()
        self.resume_data["known_languages"] = [x.strip() for x in request.form.get("known-languages", "").strip().split(",") if x.strip()]
        self.resume_data["linkedin_url"] = request.form.get("linkedin-url", "").strip()
        self.resume_data["github_url"] = request.form.get("github-url", "").strip()
        self.resume_data["website_url"] = request.form.get("personal-website-url", "").strip()

        self.resume_data["summary"] = request.form.get("summary", "").strip()

        self.resume_data["education"] = []
        school_universities = request.form.getlist("school-university-name")
        degree_course_names = request.form.getlist("degree-course-name")
        degree_course_started_years = request.form.getlist("degree-course-started-year")
        degree_course_passed_years = request.form.getlist("degree-course-passed-year")

        for i in range(min(len(school_universities), len(degree_course_names), len(degree_course_passed_years))):
            if school_universities[i].strip() and degree_course_names[i].strip() and degree_course_passed_years[i].strip() and degree_course_started_years[i].strip():
                self.resume_data["education"].append({
                    "su_name": school_universities[i].strip(),
                    "degree_course": degree_course_names[i].strip(),
                    "year": {
                        "from":degree_course_started_years[i].strip(),
                        "to":degree_course_passed_years[i].strip()
                    },
                })

        self.resume_data["certificates"] = []
        certificate_names = request.form.getlist("certificate-name")
        certified_years = request.form.getlist("certified-year")
        
        for i in range(min(len(certificate_names), len(certified_years))):
            if certificate_names[i].strip() and certified_years[i].strip():
                self.resume_data["certificates"].append({
                    "name": certificate_names[i].strip(),
                    "year": certified_years[i].strip()
                })
        
        self.resume_data["awards_and_honors"] = []
        award_honor_names = request.form.getlist("award-honor-name")
        award_honor_years = request.form.getlist("award-honor-year")

        for i in range(min(len(award_honor_names), len(award_honor_years))):
            if award_honor_names[i].strip() and award_honor_years[i].strip():
                self.resume_data["awards_and_honors"].append({
                    "name": award_honor_names[i].strip(),
                    "year": award_honor_years[i].strip(),
                })

        self.resume_data["skills"] = []
        skill_names = request.form.getlist("skill-name")
        skill_levels = request.form.getlist("skill-level")
        
        for i in range(min(len(skill_names), len(skill_levels))):
            if skill_names[i].strip() and skill_levels[i].strip():
                self.resume_data["skills"].append({
                    "name": skill_names[i].strip(),
                    "level": skill_levels[i].strip(),
                })
        
        self.resume_data["hobbies_or_interests"] = [x.strip() for x in request.form.get("hobbies-interests","").strip().split(",") if x.strip()]    

        self.resume_data["projects"] = []
        projects_names = request.form.getlist("project-name")
        projects_source_urls = request.form.getlist("project-source-url")
        projects_demo_urls = request.form.getlist("project-demo-url")
        projects_descriptions = request.form.getlist("project-description")

        for i in range(min(len(projects_names), len(projects_source_urls), len(projects_demo_urls), len(projects_descriptions))):
            pname = projects_names[i].strip()
            psource_url = projects_source_urls[i].strip()
            pdemo_url = projects_demo_urls[i].strip()
            pdescritpion = projects_descriptions[i].strip()
            if pname and (pdemo_url or psource_url) and pdescritpion:
                self.resume_data["projects"].append({
                    "name": pname,
                    "source_url": psource_url,
                    "demo_url": pdemo_url,
                    "description": pdescritpion
                })

        self.resume_data["work_experiences"] = []
        companies_names = request.form.getlist("company-name")
        companies_locations = request.form.getlist("company-location")
        job_role_names = request.form.getlist("job-role-name")
        job_from = request.form.getlist("job-from")
        job_to = request.form.getlist("job-to")
        work_exp_more_details = request.form.getlist("work-exp-more-details")
    
        for i in range(min(len(companies_names), len(companies_locations), len(job_role_names), len(job_from), len(job_to), len(work_exp_more_details))):
            if companies_names[i].strip() and companies_locations[i].strip() and job_role_names[i].strip() and job_from[i].strip():
                self.resume_data["work_experiences"].append({
                    "company": {
                        "name": companies_names[i].strip(),
                        "location": companies_locations[i].strip()
                    },
                    "job": {
                        "name": job_role_names[i].strip(),
                        "from": job_from[i].strip(),
                        "to": (job_to[i] or "Present").strip()
                    },
                    "details": work_exp_more_details[i].strip()
                })


    def validate(self):
        if self.resume_data == {}:
            return

        if not self.resume_data["name"]:
            self.errors.append("Your name is required!")
        if len(self.resume_data["name"]) > 100:
            self.errors.append("Name must be less than 100 characters!")

        if len(self.resume_data["role_job_name"]) > 100:
            self.errors.append("Role/Job name must be less than 100 characters!")
        
        if not self.resume_data["email"]:
            self.errors.append("Your email address is required!")
        elif not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', self.resume_data["email"]):
            self.errors.append("Please enter a valid email address!")
        elif len(self.resume_data["email"]) > 100:
            self.errors.append("Email address must be less than 100 characters!")

        if self.resume_data["phone"]:
            if not self.resume_data["phone"].startswith("+"):
                self.errors.append("Your Phone number must start with '+(country_code)'.")
            else:
                try:
                    phoneobj = phonenumbers.parse(self.resume_data["phone"])
                except phonenumbers.phonenumberutil.NumberParseException:
                    self.errors.append("Enter a valid phone number or leave it blank!")
                else:
                    if phonenumbers.is_valid_number(phoneobj) is not True:
                        self.errors.append("Enter a valid phone number or leave it blank!")


        if len(self.resume_data["address"]) > 175:
            self.errors.append("Address must be less than 175 characters!")
        
        if len(self.resume_data["known_languages"]) == 0:
            self.errors.append("You must enter atleast one known language that you can speak, read and write!")
        elif len(self.resume_data["known_languages"]) > 10:
            self.errors.append("Known languages cannot contain more than 10 languages!")

        for item in self.resume_data["education"]:
            if type(item["year"]["from"]) == int:
                item["year"]["from"] = str(item["year"]["from"])
            if type(item["year"]["to"]) == int:
                item["year"]["to"] = str(item["year"]["to"])
            if len(item["su_name"]) > 120:
                self.errors.append("School/University name must be than 120 characters!")
            if len(item["degree_course"]) > 120:
                self.errors.append("Degree/Course name must be than 120 characters!")
            if item["year"]["from"].isnumeric() is not True or len(item["year"]["from"].strip("-")) != 4:
                self.errors.append("Degree or Course started year must be a Number!")
            else:
                item["year"]["from"] = int(item["year"]["from"])
            if item["year"]["to"].isnumeric() is not True or len(item["year"]["to"].strip("-")) != 4:
                self.errors.append("Degree or Course passed year must be a Number!")
            else:
                item["year"]["to"] = int(item["year"]["to"])
            

        for item in self.resume_data["certificates"]:
            if type(item["year"]) == int:
                item["year"] = str(item["year"])
            if len(item["name"]) > 120:
                self.errors.append("Certificate name must be less than 120 characters!")
            if item["year"].isnumeric() is not True or len(item["year"]) != 4:
                self.errors.append("Certificate year must be a Number!")
            else:
                item["year"] = int(item["year"])

        for item in self.resume_data["awards_and_honors"]:
            if type(item["year"]) == int:
                item["year"] = str(item["year"])
            if item["year"].isnumeric() is not True or len(item["year"]) != 4:
                self.errors.append("Award/Honor year must be a Number!")
            else:
                item["year"] = int(item["year"])

        for item in self.resume_data["skills"]:
            if type(item["level"]) == int:
                item["level"] = str(item["level"])
            if len(item["name"]) > 60:
                self.errors.append("Skill name must be less than 60 characters!")
            if type(item["level"]) == int:
                item["level"] = str(item["level"])
            if item["level"].lstrip("-").isnumeric() is not True:
                self.errors.append("Skill level must be a Number!")
            else:
                if item["level"].lstrip("-").isnumeric() is True:
                    item["level"] = int(item["level"])
                    if item["level"] < -1 or item["level"] > 100:
                        self.errors.append("Skill level must be between -1 to 100.")
        

        for item in self.resume_data["projects"]:
            if len(item["name"]) > 60:
                self.errors.append("Project name must be less than or equal to 60 characters!")
            if len(item["source_url"]) > 200:
                self.errors.append("Project Source URL must be less than or equal to 200 characters, use F4nsix URL shortener to make it short!")
            if len(item["demo_url"]) > 200:
                self.errors.append("Project Demo URL must be less than or equal to 200 characters, use F4nsix URL shortener to make it short!")
            if len(item["description"]) > 500:
                self.errors.append("Project description must be less than or equal to 500 characters!")
        
        for item in self.resume_data["work_experiences"]:
            if len(item["company"]["name"]) > 100:
                self.errors.append("Company name must be less than or equal to 100 characters!")
            if len(item["company"]["location"]) > 60:
                self.errors.append("Company location must be less than or equal to 60 characters!")
            if len(item["job"]["name"]) > 100:
                self.errors.append("Job name must be less than or equal to 100 characters!")
            if len(item["details"]) > 500:
                self.errors.append("Job details must be less than or equal to 500 characters!")

        self.errors = list(set(self.errors))