Steps to run this program:
- Confirm you have python installed. Later versions of make do not come with python. 
  `which python3`

- Set up a virtual environment
  - navigate to the simple_thread_challenge directory
  - Install with `python3 -m venv .venv`
  - Activate with `source .venv/bin/activate`
  - Confirm activation with `which python`. The output should show your current directory with `bin/python`


To Review this Program
- The bulk of thte logic is in `script.py`
- Confirm that I have covered the most important cases correctly by reviewing `tests/test_reimbursement.py`
- Run tests with `python -m pytest app/tests/test_reimbursement.py`
- Print scenario output with `python -m pytest -s app/tests/test_reimbursement.py`
- Let me know if you'd like a code walkthrough!


Notes:
- I have made the assumption that inputs will always be in chronological order
- I have optimized for readability and maintainability. Starting with the tests led me to a solution that stores a lot of information in memory, making it much easier to debug. At scale, memory might become more of an issue.
