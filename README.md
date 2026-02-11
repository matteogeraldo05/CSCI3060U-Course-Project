# CSCI3060U-Course-Project

## 🎯 Overview

This Banking System simulates a real-world ATM and banking infrastructure with two main components:

### Front End
- Console-based ATM interface
- Processes banking transactions in real-time
- Supports both standard (customer) and admin (employee) modes
- Outputs transaction records for batch processing

### Back End
- Overnight batch processing system
- Updates master bank accounts file
- Applies all daily transactions
- Enforces business constraints and generates error logs

⚠️ **This is an educational project and NOT production-ready**
## 🚀 Installation

### Prerequisites

- Python 3.8 or higher

### Setup

1. Clone the repository:
```bash
git clone https://github.com/matteogeraldo05/CSCI3060U-Course-Project.git
cd CSCI3060U-Course-Project
```

2. Create the data directory:
```bash
mkdir -p data
```

3. Create a sample accounts file (or use the provided template):
```bash
cp sample_accounts.txt data/current_accounts.txt
```

4. Run the ATM:
```bash
python main.py
```


## 🛠️ Development


### Agile Practices (Project Requirement)

This project follows Agile Development principles:

- ✅ Continuously maintained test suites
- ✅ Pair programming of all code (recommended)
- ✅ Simplest possible solution to every problem
- ✅ Continuous redesign and rearchitecting
- ✅ Automation in testing and integration
- ✅ Frequent integration and complete releases

## 📚 Documentation

- **project docs**: See `to_be_added.pdf`

## 👥 Contributors

- Alexis Ryan - Development Lead
- Matteo De Angelis Geraldo - Development Lead
- Thaddeus Baturensky - Development Lead
- Zain Syed - Development Lead


---

**Version**: alpha 1.1  
**Last Updated**: February 2026  