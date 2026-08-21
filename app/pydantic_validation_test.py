from pydantic import ValidationError

from schemas.resume import PersonalInformation, Resume


try:
    resume = Resume(
        personal_information=PersonalInformation(
            name="Sohail Momin",
            email="example@gmail.com",
        ),
        education = [
            {
                "degree" : 12345,
                "institution" : "ARMIET",
            }
        ],  # Intentionally wrong
    )

    print(resume)

except ValidationError as e:
    print("===== VALIDATION ERROR =====")
    print(e)