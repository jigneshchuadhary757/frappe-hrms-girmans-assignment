# HRMS Assignment — Frappe / ERPNext App
**App name:** `hrms_assignment`  
**Author:** Jignesh Chaudhary  
**Purpose:** End-to-end HRMS automation for Recruitment, Employee Lifecycle, Payroll & Tax Regimes (Old vs New) with fixtures for quick import and testing.

---

## Table of Contents
- [Summary](#summary)  
- [Prerequisites](#prerequisites)  
- [Repository Structure](#repository-structure)  
- [Quick Setup (Local bench)](#quick-setup-local-bench)  
- [Load Fixtures & Finalize Setup](#load-fixtures--finalize-setup)  
- [Features Implemented](#features-implemented)  
- [How to Test (step-by-step)](#how-to-test-step-by-step)  
- [Screenshots & Demo Guide](#screenshots--demo-guide)  
- [Submission Checklist](#submission-checklist)  
- [Troubleshooting](#troubleshooting)  
- [CI Notes](#ci-notes)  
- [License & Contact](#license--contact)

---

## Summary
This app implements a full HRMS workflow:
- Recruitment workflow & report  
- Employee lifecycle automation (Joining → Probation → Confirmed → Exit) with Experience Letter PDF generation  
- Salary components, two salary structures (Old & New regime)  
- Payroll Entry for multiple employees and branded payslip print format  
- Employee Investment Declaration for tax exemptions and server-side integration  
- Tax Regime Comparison script report (Old vs New)  
All customizations are exported as fixtures so the app can be installed and tested quickly by the interviewer.

---

## Prerequisites
- Ubuntu (recommended) or macOS dev environment  
- Frappe & ERPNext installed (tested with Frappe/ERPNext v14.x)  
- Python 3.10+  
- MariaDB (server)  
- Redis, Node.js/npm, yarn (for front-end assets)  
- bench CLI installed

---

## Repository Structure (relevant)
apps/hrms_assignment/
├─ hrms_assignment/
│ ├─ fixtures/
│ ├─ hrms_assignment/
│ │ ├─ doctype/
│ │ ├─ report/
│ │ ├─ public/images/
│ │ └─ custom_scripts/
│ ├─ hooks.py
│ └─ README.md <-- (this file)

## Quick Setup (Local bench)
1. Clone repo inside your bench apps folder:
```bash
cd ~/frappe-bench/apps
git clone https://github.com/jigneshchuadhary757/frappe-hrms-girmans-assignment.git

## Install dependencies & build (from bench root)
cd ~/frappe-bench
bench setup requirements
bench build

## Install the app on your site:

bench --site your-site-name install-app hrms_assignment

Export (if you changed fixtures locally and want to refresh):

bench --site your-site-name export-fixtures

Features Implemented

Part 1 — Recruitment

Workflow: Recruitment Workflow (Job Opening → Application → Screening → Interview → Offer → Hired/Rejected)

Roles: HR Manager, Interviewer, Hiring Manager

Custom field on Job Applicant: Source of Application

Report: Job Applicants by Source

Part 2 — Employee Lifecycle

Workflow: Employee Lifecycle (Joining → Probation → Confirmed → Exit)

Auto-update employee status on Confirmed/Exit

Experience Letter PDF generated and attached on Exit (background job via frappe.enqueue)

Part 3 — Salary & Payroll

Salary components: Basic, HRA, Special Allowance, Provident Fund, Professional Tax

Salary Structures: Old Regime Structure, New Regime Structure

Payroll Entry automation for multiple employees

Custom payslip print format: Branded Payroll Slip

Part 4 — Tax Regime

Custom field: custom_tax_regime_preference on Employee (Old Regime / New Regime)

Auto-assign salary structure based on employee preference in Payroll Entry

Script Report: Tax Regime Comparison (Old vs New tax/deductions)

Part 5 — Customization

Doctype: Employee Investment Declaration (80C, 80D, Other exemptions, total auto-calculated)

Server Script: Adjusts taxable income on Salary Slip using investment declaration