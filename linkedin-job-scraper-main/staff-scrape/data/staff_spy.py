from pathlib import Path
from staffspy import LinkedInAccount, SolverType

session_file = Path(__file__).resolve().parent / "session.pkl"
account = LinkedInAccount(
    # credentials - remove these to sign in with browser
    # username="myemail@gmail.com",
    # password="mypassword",
    solver_api_key="CAP-6D6A8CE981803A309A0D531F8B4790BC", # optional but needed if hit with captcha
    solver_service=SolverType.CAPSOLVER,

    session_file=str(session_file), # save login cookies to only log in once (lasts a week or so)
    log_level=1, # 0 for no logs
)

# search by company
staff = account.scrape_staff(
    company_name="vietcombank",
    search_term="",
    location="",
    extra_profile_data=True, # fetch all past experiences, schools, & skills
    max_results=1000, # can go up to 1000
)
# or fetch by user ids
# users = account.scrape_users(
#     user_ids=['fuongfotfet','thuc-lien-nguyen']
# )
staff.to_csv("Vietcombank.csv", mode = 'a', header=False, index=False)
# users.to_csv("users.csv", index=False)