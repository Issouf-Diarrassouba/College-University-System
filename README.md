
End point: instructor-1.cq4bugepeexy.us-east-1.rds.amazonaws.com

# Group 12 Final Project - Phase 2

## Overview

This project represents the second phase of a comprehensive academic management system developed by Group 12. The system consists of three integrated modules:

- **APPS**: Application submission and review
- **REGS**: Student course registration and academic management
- **ADS**: Advising and degree auditing

The system supports users including applicants, students, faculty, graduate secretaries, and system administrators.

## Visual Demonstration

### APPS
- [Video 1: Completing All Application Requirements & Getting Reviewed](https://drive.google.com/file/d/13neM7dKtocaN4S8Qs1jLJvaHmPopFOHB/view?usp=share_link)
- [Video 2: Accepting Admission and Logging into Student Dashboard](https://drive.google.com/file/d/1d77yclYhWOEXcDsdZYtPRlVEQnOwpvGw/view?usp=share_link)

### REGS
- [REGS Demo Folder](https://drive.google.com/drive/folders/1m94eq-Qu0X3XR7n5eQRjX1j6Dif9E_rp?usp=sharing)

### ADS
- [Advising Demo Video](https://drive.google.com/file/d/1-KpX35LTa7CRmj_11nAjFK8XHYGWx2fe/view?usp=sharing)

## Design Justification

### Integration: APPS & REGS

From the APPS perspective, integration was achieved by inserting `degreeType` and `userType` directly into the database, enabling a seamless transition from applicant to student. The payment dropdown allowed automated updates of user type based on the deposit amount. Once admitted, users lose access to the applicant dashboard and are redirected to their student dashboard.

### Integration: REGS & ADS

From the ADS perspective, significant schema changes were required. The Phase 1 schema was restrictive, so the REGS version adopted a more flexible structure using the `c_history` table. New tables were introduced for alumni and faculty to improve data extraction and user functionality.

## Special Features & Work Breakdown

### General Contributions

- SQL table setup
- Debugging and bug fixes
- Route protection

### Talia (ADS Lead)

- GPA calculation and auditing tools
- Form 1 & transcript checks
- Dummy data insertion
- PhD workflow and thesis tracking
- Error handling
- CSS styling
- Faculty and alumni table integration
- Database updates
- Grad request approval
- Prerequisite checks

### James (REGS Lead)

- Course enrollment with prerequisite, time conflict, and repeat checks
- Course drop functionality
- Transcript view
- Advising form submission and approval
- Grade assignment
- Search bar implementation
- Admin-level permissions
- SQL schema setup and dummy data
- Styling (student and faculty pages)

### Issouf (APPS Lead)

- Full front-end and back-end for APPS module
- User creation (Applicants, Workers, System Admin)
- Worker roles and authority levels
- Application creation, update, and review
- Transcript and recommendation letter submission
- Applicant statistics generation (by Sys Admin & GS)
- SQL implementation for APPS tables
- Styling for APPS pages
- Merchandise purchasing feature (in progress)
- Role-based access control for user types
Phase 2 Report:
https://docs.google.com/document/d/1H0B6WO2opHgK-sx45gbh6L4xdNvCTnQisky5iUT7GNY/edit?usp=sharing

Login Info: 
Advisor, Reviewer:
Email/Username: bn@mcu.edu pswd: adminpass
CAC
Email/Username: elvis@mcu.edu pswd: adminpass
Advisor:
email/username: choi@mcu.edu pswd: adminpass
email/username: parmer@mcu.edu pswd: adminpass
Grad Secretary:
Email/Username: drpepper@mcu.edu pswd: adminpass

Billie: 
email/username: billie@mcu.edu pswd: adminpass

Diana Krall:
email/username: diana@mcu.edu pswd: adminpass

John Lennon: 
email/username: johnlennon@mcu.edu pswd: adminpass
Ringo Starr(APPS STARTING DATA)
email/username: ringo@mcu.edu pswd: adminpass
Paul McCarthy: 
email/username: paul@mcu.edu pswd: adminpass
Ringo2 Starr: 
email/username: ringo2@mcu.edu pswd: adminpass
Eric Clapton
email/username: eric@mcu.edu pswd: adminpass
# College-University-System
