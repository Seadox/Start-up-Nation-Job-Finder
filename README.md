# Start-up Nation Job Finder

<p align="center">
  <img src="./images/detective.png">
</p>

**Start-up Nation Job Finder** helps you search for jobs on LinkedIn. You can use it to avoid seeing job posts you don't like by using a blacklist and a wordlist. The blacklist hides job posts you want to skip, and the wordlist helps you find jobs that match what you want.

Also, **Start-up Nation Job Finder** has a big list of over 6,000 Israeli high-tech companies from the website [Start-Up Nation Central](https://startupnationcentral.org/). This can give you more information about the startup world.

# Installation

1. Clone or download the repository to your local machine.
2. Ensure you have Python 3.x installed on your system.
3. Install the required packages using the following command:

```bash
pip install -r requirements.txt
```

# Running the Program

To run the program, execute the following command:

```bash
python .\JobFinder.py -u yourlinkedinemail@email.com -p yourlinkedinpassword
```

Help:

```bash
usage: Start-up Nation Job Finder [-h] -u USERNAME -p PASSWORD [-wl WORDLIST] [-bl BLACKLIST] [-o OUTPUT]

options:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Linkedin username
  -p PASSWORD, --password PASSWORD
                        Linkedin password
  -wl WORDLIST, --wordlist WORDLIST
                        world list filter
  -bl BLACKLIST, --blacklist BLACKLIST
                        black list filter
  -o OUTPUT, --output OUTPUT
                        output file path
```

Output:

All the job posts will be saved in a CSV file, which you can easily open and view using software like Excel.
For example:

| Check | ID         | Company | Title                     | Location                                 | Link                                                          | Funding Stage | Is Remote |
| ----- | ---------- | ------- | ------------------------- | ---------------------------------------- | ------------------------------------------------------------- | ------------- | --------- |
|       | 3687474739 | Fiverr  | Platform Backend Engineer | Tel Aviv-Yafo, Tel Aviv District, Israel | https://www.linkedin.com/jobs/search/?currentJobId=3687474739 | Public        | FALSE     |

# Contributing

Contributions are welcome! If you have ideas for improvements or find any issues, please open an issue or create a pull request in this repository.

# Please Note

This program uses LinkedIn's unofficial API, and I am not liable for any associated risks, damages, or account issues that may arise from its usage.
