"""Week 2, Sunday: read Opportunities from a Salesforce Developer Edition org.

Setup:
  1. Sign up (free): https://developer.salesforce.com/signup
  2. In Salesforce: your avatar > Settings > Reset My Security Token. It arrives by email.
  3. Put SF_USERNAME, SF_PASSWORD, SF_SECURITY_TOKEN in .env.
  4. pip install simple-salesforce python-dotenv

Developer Edition orgs come with sample Accounts and Opportunities.

Run:  python week02/sf_query.py
Done when: it prints 5 opportunities with name, stage, amount and close date.
Docs: https://simple-salesforce.readthedocs.io/en/latest/user_guide/queries.html
"""
import os

from dotenv import load_dotenv
from simple_salesforce import Salesforce

load_dotenv()


def main():
    sf = Salesforce(
        username=os.environ["SF_USERNAME"],
        password=os.environ["SF_PASSWORD"],
        security_token=os.environ["SF_SECURITY_TOKEN"],
    )
    # TODO 1: write SOQL: SELECT Id, Name, StageName, Amount, CloseDate, Account.Name
    #         FROM Opportunity ORDER BY Amount DESC NULLS LAST LIMIT 5
    # TODO 2: result = sf.query(soql); loop over result["records"] and print a neat line per row
    # TODO 3 (stretch): count opportunities by StageName with a GROUP BY query
    raise NotImplementedError


if __name__ == "__main__":
    main()
