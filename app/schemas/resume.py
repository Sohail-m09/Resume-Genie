from pydantic import BaseModel, Field

class PersonalInformation(BaseModel):
    name : str | None = None
    email : str | None = None
    phone : str | None = None
    location : str | None = None
    linkedin : str | None = None
    github : str | None = None

class Education(BaseModel):
    degree: str | None = None
    institution: str | None = None
    field_of_study: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    grade: str | None = None

class Experience(BaseModel):
    company: str | None = None
    role: str | None = None
    location: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    description: list[str] = Field(default_factory=list)

class Project(BaseModel):
    name: str | None = None
    description: str | None = None
    technologies: list[str] = Field(default_factory=list)
    url: str | None = None

class Resume(BaseModel):
    personal_information: PersonalInformation
    summary: str | None = None
    skills: list[str] = Field(default_factory=list)
    education: list[Education] = Field(default_factory=list)
    experience: list[Experience] = Field(default_factory=list)
    projects: list[Project] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list) 
    