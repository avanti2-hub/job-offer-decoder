import random
import re
from openenv.core.env_server import Environment, Action, Observation, State
from models import JobOfferAction, JobOfferObservation, JobOfferState



def normalize_score(score: float) -> float:
    """
    Ensures score is strictly between (0,1)
    required by OpenEnv validator
    """
    if score <= 0:
        return 0.01
    if score >= 1:
        return 0.99
    return round(score, 2) 
# ============================================================
# EASY TASKS
# Single trap per letter but written in dense legal language
# 6 varied letters
# ============================================================

EASY_TASKS = [
    {
        "offer_text": """
PRIVATE & CONFIDENTIAL
LETTER OF APPOINTMENT
Ref: HR/2024-25/TCI/0892          Date: 15th March 2024

Mr. Rahul Sharma
B-204, Shivaji Nagar, Pune - 411005

Dear Mr. Sharma,

TechCorp India Private Limited ("Company") is pleased 
to offer you the position of Software Engineer (Grade B2) 
at our Pune Development Centre, subject to the terms 
and conditions set forth herein.

1. COMPENSATION
   Your annual Cost to Company (CTC) shall be 
   Rs. 6,00,000 as detailed in Annexure A.

2. PROBATION PERIOD
   You shall serve a probationary period of six (6) 
   months, during which performance shall be reviewed 
   monthly.

3. HUMAN CAPITAL INVESTMENT & SERVICE COVENANT
   The Company shall make substantial investments in 
   your professional integration through structured 
   technical immersion programmes, proprietary 
   methodology training, and supervised client 
   engagement. In consideration of and as a condition 
   precedent to such investment, you hereby irrevocably 
   covenant, warrant, and undertake that you shall 
   remain in the uninterrupted, full-time, exclusive 
   employment of the Company for a minimum continuous 
   period of twenty-four (24) calendar months computed 
   from your date of joining. 
   
   In the event of your voluntary separation, abandonment 
   of employment, or constructive resignation prior to 
   the expiration of the aforesaid minimum service 
   tenure, you shall, without any further notice or 
   demand, become immediately liable to pay to the 
   Company a sum of Rs. 1,50,000 (Rupees One Lakh 
   Fifty Thousand Only) as a genuine pre-estimate of 
   the liquidated damages suffered by the Company on 
   account of such premature separation. The Company 
   shall be entitled to recover this sum from your 
   Full & Final Settlement, by invoking your guarantor 
   obligations if any, or through such legal recourse 
   as may be available under applicable law.

4. ENTIRE AGREEMENT
   This letter, together with its Annexures, constitutes 
   the entire agreement between the parties.

Priya Mehta | Head - Human Resources
TechCorp India Private Limited
""",
        "has_bond": True,
        "bond_duration_months": 24,
        "bond_penalty": 150000,
        "traps": ["training_bond"],
        "trap_details": {
            "training_bond": {
                "description": "24 month bond with Rs. 1,50,000 penalty",
                "financial_impact": 150000,
                "keywords": ["liquidated damages", "minimum service", "covenant"]
            }
        }
    },
    {
        "offer_text": """
CONFIDENTIAL
OFFER OF EMPLOYMENT
Reference: DS/HR/2024/JD/441

Ms. Priya Patel
C-12, Green Park Colony, Bangalore - 560038

DataSoft Solutions LLP ("Organization") offers you 
the position of Junior Software Developer (Level L1).

ARTICLE 1 — REMUNERATION
Total annual remuneration: Rs. 5,50,000 per annum CTC.

ARTICLE 2 — PROBATION
Six (6) months probationary period from date of joining.

ARTICLE 3 — ORGANIZATIONAL COMMITMENT COVENANT
In express acknowledgment of the substantial financial, 
temporal, and intellectual resources — encompassing but 
not limited to recruitment expenditure, background 
verification costs, pre-joining orientation, structured 
onboarding programmes, technical upskilling initiatives, 
and senior mentorship allocation — that the Organization 
shall deploy exclusively towards your professional 
integration and development, you hereby unconditionally, 
irrevocably, and without reservation agree to maintain 
an uninterrupted employment relationship with the 
Organization for a minimum period of eighteen (18) 
consecutive calendar months.

Should you elect to voluntarily terminate, abandon, 
or otherwise prematurely conclude your employment 
prior to the completion of the aforesaid commitment 
period, you shall, within fifteen (15) days of 
separation, remit to the Organization a sum of 
Rs. 75,000 (Rupees Seventy-Five Thousand Only) as 
a genuine pre-estimate of liquidated damages, which 
the parties expressly agree shall not be characterized 
as a penalty or forfeiture. 

The Organization expressly reserves the right to 
withhold issuance of your relieving letter, service 
certificate, experience letter, and Full & Final 
Settlement computation until complete satisfaction 
of this obligation.

ARTICLE 4 — GENERAL SERVICE CONDITIONS
Standard leave, insurance, and benefit entitlements 
per Organization HR Policy Manual.

Authorized Signatory | Human Resources
DataSoft Solutions LLP
""",
        "has_bond": True,
        "bond_duration_months": 18,
        "bond_penalty": 75000,
        "traps": ["training_bond"],
        "trap_details": {
            "training_bond": {
                "description": "18 month bond with Rs. 75,000 penalty",
                "financial_impact": 75000,
                "keywords": ["liquidated damages", "commitment period", "withhold relieving letter"]
            }
        }
    },
    {
        "offer_text": """
LETTER OF OFFER
GreenTech Analytics Private Limited

Date: 20th March 2024
Ref: GT/PUN/2024/DA/089

Mr. Arjun Nair, Kothrud, Pune - 411038

Subject: Offer — Data Analyst (Grade A1)

1. COMPENSATION: Rs. 7,00,000 CTC per annum.

2. TERMS OF EMPLOYMENT
   2.1 Working hours: 9:00 AM to 6:00 PM, Mon-Fri.
   2.2 Annual Leave: 15 days paid, 7 days sick.
   2.3 Notice Period: 30 days written notice.
   2.4 Group Medical Insurance: Rs. 3,00,000 coverage.
   2.5 Performance reviews annually per Company policy.
   2.6 No minimum service obligation or retention bond 
       of any nature shall apply to this engagement.

3. ACCEPTANCE: Sign and return within 10 days.

Sunita Krishnamurthy | VP Human Capital
GreenTech Analytics Private Limited
""",
        "has_bond": False,
        "bond_duration_months": 0,
        "bond_penalty": 0,
        "traps": [],
        "trap_details": {}
    },
    {
        "offer_text": """
APPOINTMENT LETTER
Horizon Digital Services Private Limited
Ref: HDS/HR/2024/FE/0229

Mr. Vikram Iyer
Andheri West, Mumbai - 400053

Dear Mr. Iyer,

We are pleased to offer you the role of 
Frontend Engineer at our Mumbai office.

COMPENSATION: Rs. 8,50,000 per annum CTC.

LOCATION COMMITMENT & TRANSFER CLAUSE
You acknowledge that the Company operates 
across multiple locations in India and 
internationally. Your initial posting shall 
be Mumbai. However, the Company reserves 
the absolute and unconditional right to 
transfer, depute, or relocate your services 
to any office, branch, subsidiary, affiliate, 
or client site of the Company, whether within 
India or abroad, at any time during your 
employment, with 15 days notice. Refusal to 
relocate as directed shall constitute a breach 
of this agreement and grounds for termination 
without notice or severance.

TRAINING RECOVERY CLAUSE
In view of the Company's investment in your 
technical onboarding and role-specific training, 
should you voluntarily resign within thirty-six 
(36) months of joining, you shall be liable to 
pay Rs. 2,00,000 as training cost recovery, 
regardless of when during the 36-month period 
you resign. This amount shall be deducted from 
your Full & Final Settlement.

NOTICE PERIOD: 60 days post confirmation.

HR Department | Horizon Digital Services
""",
        "has_bond": True,
        "bond_duration_months": 36,
        "bond_penalty": 200000,
        "traps": ["training_bond", "forced_relocation"],
        "trap_details": {
            "training_bond": {
                "description": "36 month bond — longest possible, Rs. 2,00,000 penalty",
                "financial_impact": 200000,
                "keywords": ["training cost recovery", "36 months", "voluntarily resign"]
            },
            "forced_relocation": {
                "description": "Company can transfer anywhere in India or abroad with 15 days notice. Refusal = termination.",
                "financial_impact": 0,
                "keywords": ["transfer", "relocate", "15 days", "refusal", "termination"]
            }
        }
    },
    {
        "offer_text": """
OFFER LETTER
SwiftCode Technologies Private Limited
Ref: SCT/HR/2024/BE/0891

Ms. Ananya Krishnan
Koramangala, Bangalore - 560034

POSITION: Backend Engineer — Level 2
COMPENSATION: Rs. 9,00,000 per annum CTC.

PROBATION: 6 months from date of joining.

SERVICE AGREEMENT & BOND
The Company shall sponsor your participation in 
advanced cloud certification programmes (AWS/GCP), 
proprietary software architecture training, and 
external technical workshops estimated at a cost 
of Rs. 1,20,000 per annum.

In consideration thereof, you covenant to serve 
the Company for a minimum of twenty-four (24) 
months. Early voluntary resignation shall attract 
recovery of Rs. 1,20,000 in the first year and 
Rs. 60,000 in the second year (pro-rated basis), 
recoverable from Full & Final Settlement.

MOONLIGHTING PROHIBITION
You shall not, during the term of this employment, 
whether during or outside working hours, directly 
or indirectly engage in any employment, consultancy, 
advisory, or income-generating activity for any 
person, firm, or entity other than the Company, 
without prior written approval of the management. 
Violation of this clause shall be grounds for 
immediate termination without notice or severance.

NOTICE PERIOD: 90 days post-confirmation.

Head of People | SwiftCode Technologies
""",
        "has_bond": True,
        "bond_duration_months": 24,
        "bond_penalty": 120000,
        "traps": ["training_bond", "moonlighting_ban"],
        "trap_details": {
            "training_bond": {
                "description": "Tiered bond: Rs. 1,20,000 year 1, Rs. 60,000 year 2",
                "financial_impact": 120000,
                "keywords": ["covenant", "early voluntary resignation", "pro-rated"]
            },
            "moonlighting_ban": {
                "description": "Complete ban on ANY outside work even on weekends. Violation = immediate termination.",
                "financial_impact": 0,
                "keywords": ["moonlighting", "outside working hours", "income-generating", "immediate termination"]
            }
        }
    },
    {
        "offer_text": """
LETTER OF APPOINTMENT
RapidScale Fintech Private Limited
Ref: RSF/HR/2024/DA/1129

Mr. Karan Mehta
Baner, Pune - 411045

POSITION: Data Scientist — Associate
COMPENSATION: Rs. 12,00,000 per annum CTC.

TERMS & CONDITIONS

Notice Period: Either party may terminate with 
ninety (90) calendar days advance written notice. 
The Company is not obligated to accept payment 
in lieu of notice and may require full serving 
of the notice period at its sole discretion.

Non-Solicitation: For a period of twelve (12) 
months following cessation of employment, you 
shall not directly or indirectly solicit, recruit, 
or encourage any employee of the Company to 
terminate their employment.

Intellectual Property: All work product, 
inventions, algorithms, models, code, and 
developments created during employment, whether 
or not using Company resources, shall vest 
exclusively in the Company.

No minimum service bond or training recovery 
clause shall apply to this engagement.

HR Department | RapidScale Fintech
""",
        "has_bond": False,
        "bond_duration_months": 0,
        "bond_penalty": 0,
        "traps": ["long_notice", "ip_ownership", "non_solicitation"],
        "trap_details": {
            "long_notice": {
                "description": "90 day notice — company not obligated to accept buyout",
                "financial_impact": 0,
                "keywords": ["90 days", "not obligated", "payment in lieu"]
            },
            "ip_ownership": {
                "description": "All work product even outside office hours belongs to company",
                "financial_impact": 0,
                "keywords": ["work product", "whether or not using Company resources", "vest exclusively"]
            },
            "non_solicitation": {
                "description": "Cannot recruit any colleague for 12 months after leaving",
                "financial_impact": 0,
                "keywords": ["non-solicitation", "12 months", "solicit", "recruit"]
            }
        }
    },
]

# ============================================================
# MEDIUM TASKS
# 2-3 combined traps per letter
# Financial calculations required
# ============================================================

MEDIUM_TASKS = [
    {
        "offer_text": """
COMPENSATION LETTER — STRICTLY CONFIDENTIAL
InnovateTech Solutions Private Limited

Employee: Karthik Subramaniam
Role: Software Engineer — Grade B1
Location: Chennai | Effective: 1st April 2024

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ANNUAL COMPENSATION STRUCTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Basic Salary                    Rs.  3,00,000
House Rent Allowance            Rs.  1,50,000
Special Allowance               Rs.  1,20,000
Performance Linked Incentive    Rs.  1,20,000
[Subject to KRA achievement at 
sole management discretion]
Employer PF Contribution          Rs.    36,000
[Deposited to EPFO; not take-home]
Gratuity Provision              Rs.    28,846
[Only after 5 years service]
Group Medical Insurance         Rs.    15,000
[Premium paid to insurer, not employee]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL CTC                       Rs.  7,69,846
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PERFORMANCE & INCREMENT POLICY
Annual appraisals conducted every April. 
Increment of upto thirty percent (30%) on 
Basic Salary component shall be considered 
basis performance rating, budget availability, 
and management discretion. Increment shall be 
computed exclusively on Basic Salary and not 
on Total CTC. Past increments create no 
precedent for future revisions.

TRAINING BOND
In consideration of technical training investment, 
you covenant to serve for twenty-four (24) months. 
Voluntary resignation prior to completion shall 
attract recovery of Rs. 90,000 from Full & Final 
Settlement.

Notice Period: 60 days post-confirmation.
""",
        "traps": ["inflated_ctc", "fake_increment", "training_bond"],
        "trap_details": {
            "inflated_ctc": {
                "real_fixed_annual": 570000,
                "real_monthly_inhand": 45700,
                "advertised_ctc": 769846,
                "misleading_components": [
                    "Performance Linked Incentive — conditional",
                    "Employer PF — not take-home",
                    "Gratuity — only after 5 years",
                    "Medical Insurance — paid to insurer"
                ]
            },
            "fake_increment": {
                "basic_salary": 300000,
                "increment_percent": 30,
                "real_increment": 90000,
                "perceived_increment": 230954
            },
            "training_bond": {
                "duration_months": 24,
                "penalty": 90000
            }
        }
    },
    {
        "offer_text": """
APPOINTMENT LETTER
Meridian Technologies Private Limited
Ref: MTL/HR/2024/DE/0891

Candidate: [Name]
Role: Data Engineer | Location: Hyderabad

COMPENSATION
Annual CTC: Rs. 9,60,000 (Rupees Nine Lakhs 
Sixty Thousand Only) as per Annexure B.

PROBATIONARY PERIOD
Your employment commences with a mandatory 
probationary period of six (6) calendar months. 
During probation, monthly compensation shall be 
disbursed at seventy percent (70%) of monthly 
CTC, consistent with Company policy for all 
new joiners. Full CTC becomes effective upon 
successful confirmation post-probation.

The Company reserves the right to extend 
probation by up to three (3) additional months.

JOINING INCENTIVE & CLAWBACK
A one-time Joining Bonus of Rs. 1,00,000 shall 
be paid with your first month's salary as a 
goodwill gesture to facilitate your transition.

CLAWBACK PROVISION: Should your employment be 
terminated — whether by voluntary resignation 
or for cause — within twelve (12) months of 
joining, you shall refund the Joining Bonus 
in full within 30 days of last working day. 
Unpaid amounts shall attract interest at 
eighteen percent (18%) per annum compounded 
monthly until recovery. Company may recover 
same from Full & Final Settlement.

NOTICE PERIOD: 90 days post-confirmation.
No payment-in-lieu accepted without Company 
consent at sole discretion.
""",
        "traps": ["probation_salary_cut", "clawback_bonus", "long_notice"],
        "trap_details": {
            "probation_salary_cut": {
                "advertised_monthly": 80000,
                "probation_monthly": 56000,
                "months": 6,
                "total_loss": 144000
            },
            "clawback_bonus": {
                "bonus_amount": 100000,
                "clawback_period_months": 12,
                "interest_rate": 18
            },
            "long_notice": {
                "notice_days": 90,
                "market_standard": 30,
                "payment_in_lieu": "Not guaranteed — company discretion"
            }
        }
    },
    {
        "offer_text": """
TOTAL REWARDS STATEMENT
RapidGrow Ventures Private Limited

Candidate: Sneha Joshi
Role: Business Analyst | Location: Mumbai

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
YOUR TOTAL REWARDS PACKAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Basic Salary (Annual)           Rs.  2,40,000
Dearness Allowance              Rs.    60,000
Conveyance Reimbursement        Rs.    24,000
One-Time Joining Bonus*         Rs.  1,00,000
Quarterly Variable Pay**        Rs.    96,000
Employer ESI Contribution***    Rs.    15,600
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL CTC                       Rs.  5,35,600
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*One-time only; subject to clawback if 
 employment ends within 12 months for any reason
**Subject to quarterly business performance; 
  not guaranteed
***Paid to ESIC; not credited to employee

VARIABLE PAY CONDITIONS
Quarterly PLI disbursement requires:
(a) Individual rating minimum 3.5/5.0
(b) Team performance above 75th percentile
(c) Company quarterly revenue target met
(d) No active disciplinary proceedings
All four conditions must be simultaneously 
satisfied. Pro-rata payment not applicable.

INCREMENT POLICY
Annual increment of upto 25% on Basic Salary 
only, subject to budget and management approval. 
No minimum increment guaranteed.

WORK ARRANGEMENT
This role requires six (6) day work week, 
Monday through Saturday, 9AM to 7PM.
Sunday off.
""",
        "traps": ["inflated_ctc", "variable_pay_trap", "six_day_week", "fake_increment"],
        "trap_details": {
            "inflated_ctc": {
                "real_fixed_annual": 324000,
                "real_monthly_inhand": 27000,
                "advertised_ctc": 535600,
                "misleading_components": [
                    "Joining Bonus — one-time not recurring",
                    "Variable Pay — conditional on 4 criteria",
                    "ESI — paid to government not employee"
                ]
            },
            "variable_pay_trap": {
                "advertised_variable": 96000,
                "realistic_variable": 38400,
                "conditions": 4,
                "realistic_payout_percent": 40
            },
            "six_day_week": {
                "description": "6 days/week, 9AM-7PM = 60 hours/week",
                "industry_standard": "5 days/week, 9AM-6PM = 45 hours/week",
                "extra_hours_per_week": 15
            },
            "fake_increment": {
                "basic_salary": 240000,
                "increment_percent": 25,
                "real_increment": 60000,
                "perceived_increment": 133900
            }
        }
    },
    {
        "offer_text": """
OFFER OF EMPLOYMENT
BrightFuture Consulting Private Limited
Reference: BFC/HR/2024/BC/0129

Role: Business Consultant | Mumbai
Annual CTC: Rs. 8,50,000

COMPENSATION STRUCTURE
Fixed CTC:             Rs. 7,50,000
Performance Bonus:     Rs. 1,00,000
[Subject to individual and company 
performance at management discretion]

JOINING BONUS: Rs. 1,00,000 payable month 1.
Recovery: Full refund required if leaving 
within 12 months. Interest at 18% per annum 
on unpaid amounts.

PROBATION SALARY
During 6-month probation: 75% of monthly CTC.
Monthly during probation: Rs. 53,125
Monthly post-confirmation: Rs. 70,833

INTELLECTUAL PROPERTY
All work product created during employment, 
whether or not during working hours, whether 
or not using personal equipment, shall vest 
exclusively in the Company. This includes 
freelance projects, personal applications, 
and any code or creative work.

NOTICE PERIOD: 60 days. Company may require 
full serving without payment-in-lieu option.
""",
        "traps": [
            "clawback_bonus",
            "probation_salary_cut",
            "ip_ownership",
            "performance_bonus_illusion"
        ],
        "trap_details": {
            "clawback_bonus": {
                "bonus_amount": 100000,
                "clawback_period_months": 12,
                "interest_rate": 18
            },
            "probation_salary_cut": {
                "advertised_monthly": 70833,
                "probation_monthly": 53125,
                "months": 6,
                "total_loss": 106250
            },
            "ip_ownership": {
                "covers_personal_work": True,
                "covers_outside_hours": True,
                "post_employment_months": 0
            },
            "performance_bonus_illusion": {
                "bonus_amount": 100000,
                "guaranteed": False,
                "realistic_payout": 40000
            }
        }
    },
    {
        "offer_text": """
COMPENSATION LETTER
Pinnacle Financial Technologies Limited

Role: Associate Software Engineer
Annual CTC: Rs. 10,42,154

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Fixed Base Salary           Rs.  8,00,000
PLI (Performance Incentive) Rs.  2,00,000
Employer PF                 Rs.    96,000
Gratuity                    Rs.    46,154
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total CTC                   Rs. 10,42,154
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PLI CONDITIONS (all must be met simultaneously):
(a) Individual rating: minimum 3.5/5.0
(b) Team score: above 75th percentile  
(c) Company revenue: minimum 90% of target
(d) No disciplinary action during period
(e) No PIP during assessment period
(f) Full quarter employment (no pro-rata)
PLI not guaranteed. Past payment no precedent.

INCREMENT: Upto 30% on Basic Salary only.
Real increment range: Rs. 0 to Rs. 2,40,000.

TRAINING BOND: 18 months service commitment.
Early exit penalty: Rs. 1,50,000.

NOTICE: 90 days. Payment-in-lieu at Company 
discretion only.
""",
        "traps": [
            "inflated_ctc",
            "variable_pay_trap",
            "fake_increment",
            "training_bond",
            "long_notice"
        ],
        "trap_details": {
            "inflated_ctc": {
                "real_fixed_annual": 800000,
                "real_monthly_inhand": 63500,
                "advertised_ctc": 1042154,
                "misleading_components": [
                    "PLI — conditional on 6 criteria",
                    "Employer PF — not take-home",
                    "Gratuity — only after 5 years"
                ]
            },
            "variable_pay_trap": {
                "advertised_variable": 200000,
                "realistic_variable": 80000,
                "conditions": 6,
                "realistic_payout_percent": 40
            },
            "fake_increment": {
                "basic_salary": 800000,
                "increment_percent": 30,
                "real_increment": 240000,
                "note": "On basic only, not total CTC"
            },
            "training_bond": {
                "duration_months": 18,
                "penalty": 150000
            },
            "long_notice": {
                "notice_days": 90,
                "payment_in_lieu": "Company discretion only"
            }
        }
    },
    {
        "offer_text": """
APPOINTMENT LETTER
GlobalSystems India Private Limited
Ref: GSI/HR/2024/SDE/2341

Role: Software Development Engineer II
Annual CTC: Rs. 14,00,000

COMPENSATION BREAKDOWN
Fixed Salary:          Rs. 11,20,000
Annual Variable:       Rs.  2,80,000
[20% of CTC; performance-based]

PROBATION: 6 months at 80% of monthly CTC.
Monthly during probation: Rs. 93,333
Monthly post-confirmation: Rs. 1,16,667

NOTICE PERIOD: 90 days. Company reserves 
right to require full notice period. Not 
obligated to accept payment-in-lieu.

MOONLIGHTING PROHIBITION
No outside employment, freelancing, consulting, 
or income-generating activity permitted during 
employment, whether during or outside work hours.

INTELLECTUAL PROPERTY
All inventions, code, writings during employment 
AND twelve (12) months post-employment belong 
to Company if related to Company's business domain.

JURISDICTION: All disputes — Delhi courts only.
Employee work location: Pune.
""",
        "traps": [
            "probation_salary_cut",
            "variable_pay_trap",
            "long_notice",
            "moonlighting_ban",
            "ip_ownership",
            "arbitration_trap"
        ],
        "trap_details": {
            "probation_salary_cut": {
                "advertised_monthly": 116667,
                "probation_monthly": 93333,
                "months": 6,
                "total_loss": 140000
            },
            "variable_pay_trap": {
                "advertised_variable": 280000,
                "realistic_variable": 112000,
                "conditions": 4,
                "realistic_payout_percent": 40
            },
            "long_notice": {
                "notice_days": 90,
                "market_standard": 30
            },
            "moonlighting_ban": {
                "covers_weekends": True,
                "covers_personal_time": True
            },
            "ip_ownership": {
                "covers_outside_hours": True,
                "post_employment_months": 12
            },
            "arbitration_trap": {
                "employee_location": "Pune",
                "dispute_city": "Delhi",
                "distance_km": 1400
            }
        }
    },
]

# ============================================================
# HARD TASKS
# 4-5 combined traps including advanced legal traps
# Requires deep legal + financial analysis
# ============================================================

HARD_TASKS = [
    {
        "offer_text": """
EMPLOYMENT AGREEMENT
Quantum Dynamics Technology Private Limited
Ref: QDT/HR/2024/SWE/0441

Role: Senior Software Engineer
Annual CTC: Rs. 18,00,000

SECTION 1 — COMPENSATION
Fixed: Rs. 14,40,000 | Variable: Rs. 3,60,000
Variable subject to management discretion.

SECTION 2 — PROBATION
6 months at 70% of CTC = Rs. 1,05,000/month
Full salary: Rs. 1,50,000/month post-confirmation.
Loss during probation: Rs. 2,70,000.

SECTION 3 — INTELLECTUAL PROPERTY ASSIGNMENT
You hereby irrevocably assign to the Company 
all right, title, and interest in all Work 
Product — inventions, code, algorithms, 
designs, writings — that you conceive, develop, 
or create:
(a) During employment, whether or not during 
    working hours;
(b) Using personal equipment outside office;
(c) Related to Company's current or 
    anticipated business areas;
(d) During the twelve (12) months FOLLOWING 
    cessation of employment.

You must disclose all personal projects to 
the Company within 30 days of creation.

SECTION 4 — GARDEN LEAVE & NOTICE
Notice Period: 90 calendar days.
Company may place you on Garden Leave during 
notice — you receive salary but cannot join 
any employer or engage in any business 
activity. Payment-in-lieu not available as 
of right; Company discretion only.

SECTION 5 — POST-EMPLOYMENT RESTRICTIONS
(a) Non-Compete: 24 months — cannot join 
    any competing firm in India.
(b) Non-Solicitation: 12 months — cannot 
    recruit current employees.
(c) Confidentiality: Perpetual.

SECTION 6 — DISPUTE RESOLUTION
Mandatory arbitration in New Delhi. 
Arbitrator appointed solely by Company. 
Each party bears own legal costs.
Employee work location: Bangalore.

SECTION 7 — SALARY REVIEW
Annual review conducted. Increment, if any, 
at sole management discretion. No minimum 
increment guaranteed. Company may defer 
increments citing business conditions.
""",
        "traps": [
            "inflated_ctc",
            "probation_salary_cut",
            "ip_ownership",
            "garden_leave",
            "non_compete",
            "arbitration_trap",
            "salary_review_illusion"
        ],
        "trap_details": {
            "inflated_ctc": {
                "real_fixed_annual": 1440000,
                "real_monthly_inhand": 113000,
                "advertised_ctc": 1800000,
                "misleading_components": [
                    "Variable Rs. 3,60,000 — fully discretionary"
                ]
            },
            "probation_salary_cut": {
                "advertised_monthly": 150000,
                "probation_monthly": 105000,
                "months": 6,
                "total_loss": 270000
            },
            "ip_ownership": {
                "covers_outside_hours": True,
                "covers_personal_equipment": True,
                "post_employment_months": 12,
                "disclosure_required": True
            },
            "garden_leave": {
                "notice_days": 90,
                "can_join_employer_during": False,
                "payment_in_lieu_available": False
            },
            "non_compete": {
                "duration_months": 24,
                "enforceability": "Largely unenforceable under Section 27 Indian Contract Act",
                "practical_risk": "Company may threaten legal action even if unenforceable"
            },
            "arbitration_trap": {
                "employee_location": "Bangalore",
                "dispute_city": "New Delhi",
                "arbitrator_appointed_by": "Company",
                "distance_km": 2100
            },
            "salary_review_illusion": {
                "guaranteed_increment": False,
                "language": "if any — legally means zero increment possible"
            }
        }
    },
    {
        "offer_text": """
SENIOR APPOINTMENT AGREEMENT
Apex Financial Services Private Limited
Ref: AFS/HR/2024/SM/0089

Role: Senior Manager — Technology
Annual CTC: Rs. 24,00,000

COMPENSATION
Fixed: Rs. 18,00,000 annual
PLI: Rs. 6,00,000 (25% of CTC)
PLI conditions: Individual rating 4/5, 
team target, company profitability, 
no disciplinary action, full year service.
Realistic PLI payout: ~40% = Rs. 2,40,000.

PROBATION: 6 months at 75% CTC.
Monthly probation salary: Rs. 1,50,000
Monthly confirmed salary: Rs. 2,00,000
Loss in probation: Rs. 3,00,000.

JOINING BONUS: Rs. 2,00,000.
Clawback: Full refund + 18% interest if 
leaving within 18 months of joining.

GARDEN LEAVE
Notice period: 90 days. Company may impose 
Garden Leave for the full 90 days — you stay 
home, receive salary, but cannot join any 
employer. Payment-in-lieu not an employee 
right.

NON-COMPETE: 24 months post-employment — 
cannot join competing firm in India.

Combined effective lock-in post-resignation:
90 days garden leave + 24 months non-compete 
= up to 27 months before truly free.

INTELLECTUAL PROPERTY
All work during employment and 12 months 
post-employment belongs to Company.
Personal projects must be disclosed.

DISPUTE RESOLUTION
Sole arbitrator appointed by Company.
Seat: Mumbai. Employee location: Pune.
Costs borne by each party.

INCREMENT POLICY
Annual review. Increment "if any" at 
management discretion. No guarantee.
6-day work week: Monday to Saturday.
Working hours: 9AM to 8PM.
""",
        "traps": [
            "variable_pay_trap",
            "probation_salary_cut",
            "clawback_bonus",
            "garden_leave",
            "non_compete",
            "ip_ownership",
            "arbitration_trap",
            "salary_review_illusion",
            "six_day_week"
        ],
        "trap_details": {
            "variable_pay_trap": {
                "advertised_variable": 600000,
                "realistic_variable": 240000,
                "conditions": 5
            },
            "probation_salary_cut": {
                "advertised_monthly": 200000,
                "probation_monthly": 150000,
                "months": 6,
                "total_loss": 300000
            },
            "clawback_bonus": {
                "bonus_amount": 200000,
                "clawback_period_months": 18,
                "interest_rate": 18
            },
            "garden_leave": {
                "notice_days": 90,
                "effective_lock_in_months": 27
            },
            "non_compete": {
                "duration_months": 24,
                "enforceability": "Questionable under Indian law"
            },
            "ip_ownership": {
                "covers_outside_hours": True,
                "post_employment_months": 12
            },
            "arbitration_trap": {
                "employee_location": "Pune",
                "dispute_city": "Mumbai",
                "arbitrator_appointed_by": "Company"
            },
            "salary_review_illusion": {
                "guaranteed": False
            },
            "six_day_week": {
                "hours_per_week": 66,
                "industry_standard": 45
            }
        }
    },
    {
        "offer_text": """
EMPLOYMENT CONTRACT
Vertex Global Solutions Limited
Ref: VGS/HR/2024/ENG/3341

Role: Production Engineer | Location: Pune
Annual CTC: Rs. 8,50,000

COMPENSATION
Fixed: Rs. 6,80,000 | Variable: Rs. 1,70,000
[Variable: 20% on KRA achievement; not guaranteed]

PROBATION: 6 months at 70% of CTC.
Probation monthly: Rs. 49,583
Confirmed monthly: Rs. 70,833
Loss during probation: Rs. 1,27,500.

SERVICE BOND
36-month minimum service covenant.
Penalty: Rs. 2,00,000 recoverable from 
Full & Final Settlement.

MOONLIGHTING PROHIBITION
No outside work of any kind during employment, 
including weekends and personal time.
Violation = immediate termination without 
severance.

INTELLECTUAL PROPERTY  
All work product during employment and 
18 months post-employment vests in Company.
Includes personal code, freelance work, 
startup-related developments.

DISPUTE RESOLUTION
Arbitration mandatory. Seat: New Delhi.
Arbitrator: Appointed by Company.
Jurisdiction: Delhi courts exclusively.
Employee location: Pune (1400km from Delhi).

NON-COMPETE: 12 months post-employment.

INCREMENT POLICY
"Performance-linked increment, if any, at 
management discretion." Zero minimum guaranteed.

NOTICE: 90 days. Garden Leave may be imposed.
""",
        "traps": [
            "probation_salary_cut",
            "training_bond",
            "moonlighting_ban",
            "ip_ownership",
            "arbitration_trap",
            "non_compete",
            "garden_leave",
            "salary_review_illusion",
            "variable_pay_trap"
        ],
        "trap_details": {
            "probation_salary_cut": {
                "advertised_monthly": 70833,
                "probation_monthly": 49583,
                "months": 6,
                "total_loss": 127500
            },
            "training_bond": {
                "duration_months": 36,
                "penalty": 200000
            },
            "moonlighting_ban": {
                "covers_weekends": True,
                "violation_consequence": "Immediate termination"
            },
            "ip_ownership": {
                "covers_outside_hours": True,
                "post_employment_months": 18
            },
            "arbitration_trap": {
                "employee_location": "Pune",
                "dispute_city": "Delhi",
                "distance_km": 1400
            },
            "non_compete": {
                "duration_months": 12
            },
            "garden_leave": {
                "notice_days": 90
            },
            "salary_review_illusion": {
                "guaranteed": False
            },
            "variable_pay_trap": {
                "advertised_variable": 170000,
                "realistic_variable": 68000
            }
        }
    },
    {
        "offer_text": """
LETTER OF APPOINTMENT
FinanceHub Corporate Services Limited
Ref: FH/HRD/2024/AT/2291

Role: Associate Technology Analyst
Annual CTC: Rs. 12,00,000

COMPENSATION
Fixed: Rs. 9,00,000
Performance Incentive: Rs. 3,00,000
[Requires: rating 4/5, team target, 
company profit target, no disciplinary 
action, full year employment — all 
simultaneously. Past payment no precedent.]
Realistic incentive: ~35% = Rs. 1,05,000.

PROBATION: 6 months at 70% CTC.
Monthly probation: Rs. 70,000
Monthly confirmed: Rs. 1,00,000
Total probation loss: Rs. 1,80,000.

TENURE OBLIGATION
24-month minimum service. Early exit: 
Rs. 2,00,000 liquidated damages.

JOINING BONUS: Rs. 1,50,000.
Clawback: Full refund if leaving within 
15 months. Interest 18% p.a. on unpaid amount.

INTELLECTUAL PROPERTY
All work product during and 12 months 
post-employment belongs to Company.
Personal startups and freelance included.
Mandatory disclosure of personal projects.

GARDEN LEAVE
90-day notice. Garden leave may be imposed 
for full period. Cannot join employer during.
Payment-in-lieu: Company discretion only.

NON-COMPETE: 24 months post-employment.
NON-SOLICITATION: 12 months post-employment.

DISPUTE RESOLUTION
Arbitration in New Delhi. Arbitrator by Company.
Employee location: Chennai (2200km from Delhi).

SALARY REVIEW: "If any" — zero guaranteed.
WORK WEEK: Monday-Saturday, 9AM-7PM.
""",
        "traps": [
            "variable_pay_trap",
            "probation_salary_cut",
            "training_bond",
            "clawback_bonus",
            "ip_ownership",
            "garden_leave",
            "non_compete",
            "arbitration_trap",
            "salary_review_illusion",
            "six_day_week"
        ],
        "trap_details": {
            "variable_pay_trap": {
                "advertised_variable": 300000,
                "realistic_variable": 105000,
                "conditions": 5
            },
            "probation_salary_cut": {
                "advertised_monthly": 100000,
                "probation_monthly": 70000,
                "months": 6,
                "total_loss": 180000
            },
            "training_bond": {
                "duration_months": 24,
                "penalty": 200000
            },
            "clawback_bonus": {
                "bonus_amount": 150000,
                "clawback_period_months": 15,
                "interest_rate": 18
            },
            "ip_ownership": {
                "covers_outside_hours": True,
                "post_employment_months": 12
            },
            "garden_leave": {
                "notice_days": 90,
                "effective_lock_in_months": 27
            },
            "non_compete": {
                "duration_months": 24
            },
            "arbitration_trap": {
                "employee_location": "Chennai",
                "dispute_city": "Delhi",
                "distance_km": 2200
            },
            "salary_review_illusion": {
                "guaranteed": False
            },
            "six_day_week": {
                "hours_per_week": 60
            }
        }
    },
    {
        "offer_text": """
OFFER LETTER
MegaCorp Technologies Private Limited
Ref: MCT/HR/2024/SE/1829

Role: Senior Software Engineer
Annual CTC: Rs. 8,00,000

COMPENSATION
Fixed: Rs. 6,40,000 (80% of CTC)
Variable: Rs. 1,60,000 (20% of CTC)
[Variable subject to KRA + company targets]

PROBATION: 6 months at 75% of monthly CTC.
Monthly probation: Rs. 50,000
Monthly confirmed: Rs. 66,667
Probation loss: Rs. 1,00,000.

TRAINING BOND: 18 months. 
Penalty: Rs. 1,00,000 if leaving early.

NOTICE: 90 days. Garden leave applicable. 
Company not obligated to accept buyout.

NON-COMPETE: 12 months. No competing firm in India.
IP: All work during employment belongs to Company.

WORK ARRANGEMENT: Full on-site. No WFH.
WORK WEEK: Monday-Saturday.
INCREMENT: Performance-based "if any."
JURISDICTION: Delhi. Employee location: Bangalore.
""",
        "traps": [
            "variable_pay_trap",
            "probation_salary_cut",
            "training_bond",
            "garden_leave",
            "non_compete",
            "ip_ownership",
            "arbitration_trap",
            "six_day_week",
            "salary_review_illusion"
        ],
        "trap_details": {
            "variable_pay_trap": {
                "advertised_variable": 160000,
                "realistic_variable": 64000
            },
            "probation_salary_cut": {
                "advertised_monthly": 66667,
                "probation_monthly": 50000,
                "months": 6,
                "total_loss": 100000
            },
            "training_bond": {
                "duration_months": 18,
                "penalty": 100000
            },
            "garden_leave": {
                "notice_days": 90
            },
            "non_compete": {
                "duration_months": 12
            },
            "ip_ownership": {
                "covers_outside_hours": True,
                "post_employment_months": 0
            },
            "arbitration_trap": {
                "employee_location": "Bangalore",
                "dispute_city": "Delhi",
                "distance_km": 2100
            },
            "six_day_week": {
                "hours_per_week": 60
            },
            "salary_review_illusion": {
                "guaranteed": False
            }
        }
    },
    {
        "offer_text": """
APPOINTMENT LETTER
StartupY Technologies Private Limited
Ref: STY/HR/2024/PM/0441

Role: Product Manager
Annual CTC: Rs. 16,00,000

COMPENSATION
Fixed: Rs. 11,20,000
ESOP (Stock Options): Rs. 4,80,000 value
[Vest over 4 years: 25% per year.
No payout if you leave before 1 year.
Company has right to repurchase at 
par value — not market value — if 
you leave before IPO/acquisition.]

JOINING BONUS: Rs. 2,00,000.
Clawback: Full refund + 24% interest 
if leaving within 24 months.

PROBATION: 3 months at 80% CTC.
Loss during probation: Rs. 1,86,667.

MOONLIGHTING BAN: No outside work.
IP: All work during and 12 months 
post-employment belongs to Company.

GARDEN LEAVE: 60-day notice with 
garden leave option for Company.
NON-COMPETE: 18 months post-employment.

SALARY REVIEW: "If any" at discretion.
INCREMENT BASE: Basic salary only.

DISPUTE RESOLUTION
Arbitration: Mumbai. Arbitrator: Company.
Employee location: Hyderabad.
""",
        "traps": [
            "esop_trap",
            "clawback_bonus",
            "probation_salary_cut",
            "moonlighting_ban",
            "ip_ownership",
            "garden_leave",
            "non_compete",
            "arbitration_trap",
            "salary_review_illusion"
        ],
        "trap_details": {
            "esop_trap": {
                "esop_value": 480000,
                "vesting_years": 4,
                "year1_cliff": True,
                "repurchase_at_par": True,
                "risk": "Company buys back at original price, not market price"
            },
            "clawback_bonus": {
                "bonus_amount": 200000,
                "clawback_period_months": 24,
                "interest_rate": 24
            },
            "probation_salary_cut": {
                "advertised_monthly": 93333,
                "probation_monthly": 74667,
                "months": 3,
                "total_loss": 56000
            },
            "moonlighting_ban": {
                "covers_weekends": True
            },
            "ip_ownership": {
                "post_employment_months": 12
            },
            "garden_leave": {
                "notice_days": 60
            },
            "non_compete": {
                "duration_months": 18
            },
            "arbitration_trap": {
                "employee_location": "Hyderabad",
                "dispute_city": "Mumbai",
                "distance_km": 700
            },
            "salary_review_illusion": {
                "guaranteed": False
            }
        }
    },
]


# ============================================================
# MULTI-STEP GRADERS
# Step 1: Clause identification
# Step 2: Financial impact calculation
# Step 3: Recommendation & negotiation
# ============================================================

def grade_step1_identification(
    analysis: str, task_data: dict, difficulty: str
) -> float:
    """Grade how well AI identified all suspicious clauses"""

    analysis_lower = analysis.lower()
    traps = task_data.get("traps", [])

    # Case when there are NO traps in the offer
    if not traps:

        clean_words = [
            "no bond",
            "clean",
            "safe",
            "no suspicious",
            "standard",
            "fair",
            "no concerning",
            "no minimum service",
            "no retention"
        ]

        if any(w in analysis_lower for w in clean_words):
            return normalize_score(0.95)

        return normalize_score(0.35)

    # keywords for each trap
    trap_keywords = {

        "training_bond":[
            "bond","minimum service",
            "liquidated damages",
            "training recovery"
        ],

        "probation_salary_cut":[
            "probation",
            "70%","75%","80%",
            "reduced salary"
        ],

        "clawback_bonus":[
            "clawback",
            "refund bonus",
            "repay bonus",
            "interest"
        ],

        "ip_ownership":[
            "intellectual property",
            "work product",
            "outside hours"
        ],

        "garden_leave":[
            "garden leave"
        ],

        "non_compete":[
            "non compete",
            "cannot join competitor"
        ],

        "arbitration_trap":[
            "arbitration",
            "jurisdiction"
        ],

        "inflated_ctc":[
            "inflated",
            "misleading ctc"
        ],

        "variable_pay_trap":[
            "variable",
            "not guaranteed"
        ],

        "moonlighting_ban":[
            "moonlighting",
            "outside work"
        ],

        "six_day_week":[
            "6 day",
            "saturday"
        ],

        "long_notice":[
            "90 day notice"
        ],

        "forced_relocation":[
            "transfer",
            "relocate"
        ],

        "esop_trap":[
            "esop",
            "vesting"
        ]

    }

    traps_found = 0

    for trap in traps:

        keywords = trap_keywords.get(trap, [])

        if any(k in analysis_lower for k in keywords):
            traps_found += 1

    score = traps_found / len(traps)

# ensure minimum score > 0
    if score == 0:
        score = 0.05

    # avoid returning 1.0 exactly
    if score == 1.0:
        score = 0.95

    return normalize_score(score)


def grade_step2_financial_impact(
    analysis: str, task_data: dict, difficulty: str
) -> float:
    """Grade accuracy of financial impact calculations"""
    score = 0.0
    analysis_lower = analysis.lower()
    trap_details = task_data.get("trap_details", {})

    numbers_in_analysis = re.findall(r'\d+[,\d]*', analysis)
    nums_clean = set([
        int(n.replace(",", ""))
        for n in numbers_in_analysis
        if len(n.replace(",", "")) >= 4
    ])

    checks_done = 0
    checks_passed = 0

    # Check probation loss calculation
    if "probation_salary_cut" in trap_details:
        prob = trap_details["probation_salary_cut"]
        total_loss = prob.get("total_loss", 0)
        tolerance = total_loss * 0.15
        checks_done += 1
        for num in nums_clean:
            if abs(num - total_loss) <= tolerance:
                checks_passed += 1
                break

    # Check real monthly inhand
    if "inflated_ctc" in trap_details:
        ctc = trap_details["inflated_ctc"]
        real_monthly = ctc.get("real_monthly_inhand", 0)
        tolerance = real_monthly * 0.15
        checks_done += 1
        for num in nums_clean:
            if abs(num - real_monthly) <= tolerance:
                checks_passed += 1
                break

    # Check bond penalty mentioned
    if "training_bond" in trap_details:
        bond = trap_details["training_bond"]
        penalty = bond.get("penalty", 0)
        checks_done += 1
        if str(penalty).replace(",", "") in \
                analysis.replace(",", ""):
            checks_passed += 1

    # Check realistic variable pay
    if "variable_pay_trap" in trap_details:
        var = trap_details["variable_pay_trap"]
        realistic = var.get("realistic_variable", 0)
        tolerance = realistic * 0.20
        checks_done += 1
        for num in nums_clean:
            if abs(num - realistic) <= tolerance:
                checks_passed += 1
                break

    # Check clawback amount + interest mentioned
    if "clawback_bonus" in trap_details:
        cb = trap_details["clawback_bonus"]
        bonus = cb.get("bonus_amount", 0)
        interest = cb.get("interest_rate", 0)
        checks_done += 1
        has_bonus = str(bonus).replace(",", "") in \
            analysis.replace(",", "")
        has_interest = str(interest) in analysis
        if has_bonus and has_interest:
            checks_passed += 1
        elif has_bonus or has_interest:
            checks_passed += 0.5

    # Check fake increment calculation
    if "fake_increment" in trap_details:
        fi = trap_details["fake_increment"]
        real_inc = fi.get("real_increment", 0)
        tolerance = real_inc * 0.15
        checks_done += 1
        for num in nums_clean:
            if abs(num - real_inc) <= tolerance:
                checks_passed += 1
                break

    if checks_done == 0:
        # Non-financial traps — check qualitative impact
        impact_words = [
            "impact", "risk", "consequence",
            "danger", "problem", "affect",
            "cannot", "locked", "trapped"
        ]
        if any(w in analysis_lower for w in impact_words):
            return normalize_score(0.7)
        return normalize_score(0.4)

    score = checks_passed / checks_done

    # ensure score never becomes 0
    if score == 0:
        score = 0.05

    # Bonus for mentioning total cumulative impact
    total_words = [
        "total loss", "cumulative", "overall impact",
        "combined", "in total", "altogether"
    ]
    if any(w in analysis_lower for w in total_words):
        score = min(1.0, score + 0.1)

    return normalize_score(min(score, 1.0))


def grade_step3_recommendation(
    analysis: str, task_data: dict, difficulty: str
) -> float:
    """Grade quality of recommendation and negotiation strategy"""
    score = 0.0
    analysis_lower = analysis.lower()
    traps = task_data.get("traps", [])

    # Did it give a clear verdict?
    verdict_words = [
        "do not sign", "avoid", "reject",
        "sign only if", "negotiate before",
        "recommend signing", "safe to accept",
        "acceptable", "proceed with caution",
        "strongly advise against"
    ]
    if any(w in analysis_lower for w in verdict_words):
        score += 0.3

    # Did it give specific negotiation points?
    negotiate_words = [
        "negotiate", "request removal",
        "ask company to", "demand",
        "push back on", "counter-propose",
        "insist on", "request written"
    ]
    if any(w in analysis_lower for w in negotiate_words):
        score += 0.3

    # Did it prioritize which clauses to fight first?
    priority_words = [
        "most important", "priority", "first",
        "critical", "especially", "particularly",
        "above all", "most dangerous", "biggest risk"
    ]
    if any(w in analysis_lower for w in priority_words):
        score += 0.2

    # Did it give practical actionable advice?
    action_words = [
        "written confirmation", "email",
        "before signing", "legal advice",
        "employment lawyer", "document",
        "get it in writing", "red flag"
    ]
    if any(w in analysis_lower for w in action_words):
        score += 0.2

    # Bonus: mentioned non-compete
    # enforceability if relevant
    if "non_compete" in traps:
        if "section 27" in analysis_lower or \
           "unenforceable" in analysis_lower or \
           "indian contract act" in analysis_lower:
            score = min(1.0, score + 0.1)
    if score == 0:
        score = 0.05

    return normalize_score(min(score, 1.0))

    


# ============================================================
# MAIN ENVIRONMENT CLASS — 3-STEP INTERACTION
# ============================================================

class JobOfferDecoderEnvironment(Environment):

    def __init__(self):
        self._state = JobOfferState()
        self._current_task = None
        self._current_difficulty = None
        self._current_step = 0
        self._step_scores = []
        self._next_difficulty = None

    def reset(self) -> JobOfferObservation:
        if hasattr(self, '_next_difficulty') and self._next_difficulty:
            difficulty = self._next_difficulty
            self._next_difficulty = None
        else:
            difficulty = random.choice(["easy", "medium", "hard"])

        if difficulty == "easy":
            task_data = random.choice(EASY_TASKS)
        elif difficulty == "medium":
            task_data = random.choice(MEDIUM_TASKS)
        else:
            task_data = random.choice(HARD_TASKS)

        self._current_task = task_data
        self._current_difficulty = difficulty
        self._current_step = 1
        self._step_scores = []

        self._state = JobOfferState(
            episode_id=str(random.randint(10000, 99999)),
            step_count=0,
            task_type="multi_step_analysis",
            difficulty=difficulty,
        )

        instructions = (
            "STEP 1 OF 3 — CLAUSE IDENTIFICATION\n\n"
            "You are a senior employment lawyer reviewing "
            "this offer letter for a fresher candidate.\n\n"
            "Read every clause carefully. Identify and list "
            "ALL suspicious, risky, or potentially harmful "
            "clauses you find in this letter.\n\n"
            "For each clause found:\n"
            "- Name the clause type\n"
            "- Quote the exact suspicious language\n"
            "- Explain in one line why it is concerning\n\n"
            "Be thorough — missing clauses will cost points "
            "in the next steps."
        )

        return JobOfferObservation(
            done=False,
            reward=None,
            offer_text=task_data["offer_text"],
            task_type="step_1_identification",
            instructions=instructions,
            difficulty=difficulty,
        )

    def step(self, action: JobOfferAction) -> JobOfferObservation:
        self._state.step_count += 1

        if self._current_step == 1:
            # Grade Step 1
            score1 = grade_step1_identification(
                action.analysis,
                self._current_task,
                self._current_difficulty
            )
            self._step_scores.append(score1)
            self._current_step = 2

            instructions = (
                f"STEP 2 OF 3 — FINANCIAL IMPACT ANALYSIS\n\n"
                f"Step 1 Score: {score1:.2f}/1.0\n\n"
                "Now calculate the exact financial impact "
                "of each clause you identified.\n\n"
                "For each risky clause:\n"
                "- Calculate exact rupee amount at risk\n"
                "- Calculate total money lost in probation "
                "(if applicable)\n"
                "- Calculate realistic vs advertised salary\n"
                "- Calculate total cumulative financial risk\n\n"
                "Show your calculations clearly."
            )

            return JobOfferObservation(
                done=False,
                reward=score1,
                offer_text=self._current_task["offer_text"],
                task_type="step_2_financial_impact",
                instructions=instructions,
                difficulty=self._current_difficulty,
            )

        elif self._current_step == 2:
            # Grade Step 2
            score2 = grade_step2_financial_impact(
                action.analysis,
                self._current_task,
                self._current_difficulty
            )
            self._step_scores.append(score2)
            self._current_step = 3

            total_so_far = sum(self._step_scores) / \
                len(self._step_scores)

            instructions = (
                f"STEP 3 OF 3 — RECOMMENDATION & STRATEGY\n\n"
                f"Step 1 Score: {self._step_scores[0]:.2f}/1.0\n"
                f"Step 2 Score: {score2:.2f}/1.0\n\n"
                "Give your final verdict and negotiation "
                "strategy for this candidate.\n\n"
                "1. Overall verdict: Should they sign? "
                "(Yes / No / Only if negotiated)\n"
                "2. List the TOP 3 clauses to negotiate "
                "first, in order of priority\n"
                "3. For each: what exact change to demand "
                "from the company\n"
                "4. What to do if company refuses to "
                "negotiate these clauses\n"
                "5. Any Indian law references that protect "
                "the employee (e.g. non-compete "
                "enforceability under Contract Act)"
            )

            return JobOfferObservation(
                done=False,
                reward=score2,
                offer_text="",
                task_type="step_3_recommendation",
                instructions=instructions,
                difficulty=self._current_difficulty,
            )

        else:
            # Grade Step 3 — Final
            score3 = grade_step3_recommendation(
                action.analysis,
                self._current_task,
                self._current_difficulty
            )
            self._step_scores.append(score3)

            # Final score = weighted average
            # Step 1: 30%, Step 2: 35%, Step 3: 35%
            final_reward = normalize_score(
                self._step_scores[0] * 0.30 +
                self._step_scores[1] * 0.35 +
                score3 * 0.35
            )

            return JobOfferObservation(
                done=True,
                reward=final_reward,
                offer_text="",
                task_type="episode_complete",
                instructions=(
                    f"Episode Complete!\n"
                    f"Step 1 (Identification):  "
                    f"{self._step_scores[0]:.2f}\n"
                    f"Step 2 (Financial Impact): "
                    f"{self._step_scores[1]:.2f}\n"
                    f"Step 3 (Recommendation):  "
                    f"{score3:.2f}\n"
                    f"Final Score: {final_reward:.2f}/1.0"
                ),
                difficulty=self._current_difficulty,
            )

    @property
    def state(self) -> JobOfferState:
        return self._state