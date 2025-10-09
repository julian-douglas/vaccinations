seed_vaccines = [
    # --- Core Childhood ---
    {
        "name": "Hepatitis B",
        "primary_series_doses": 3,
        "price_per_dose": 32.0,
        "administration_route": "IM",
        "age_min": 0,
        "contraindications": ["Allergy to yeast"],
        "side_effects": ["Soreness", "Fatigue"],
        "notes": "Typical schedule: 0,1,6 months."
    },
    {
        "name": "DTaP (Diphtheria, Tetanus, acellular Pertussis)",
        "primary_series_doses": 5,
        "booster_interval_years": 10.0,
        "price_per_dose": 28.0,
        "administration_route": "IM",
        "age_min": 0.17,
        "contraindications": ["Encephalopathy after previous dose"],
        "side_effects": ["Fever", "Irritability"],
        "notes": "Pediatric formulation; boosters later with Tdap/Td."
    },
    {
        "name": "IPV (Inactivated Polio Vaccine)",
        "primary_series_doses": 4,
        "price_per_dose": 20.0,
        "administration_route": "IM",
        "age_min": 0.17,
        "contraindications": ["Severe allergy to neomycin/streptomycin"],
        "side_effects": ["Soreness"],
        "notes": "Often combined in combo vaccines."
    },
    {
        "name": "Haemophilus influenzae type b (Hib)",
        "primary_series_doses": 4,
        "price_per_dose": 22.0,
        "administration_route": "IM",
        "age_min": 0.17,
        "contraindications": ["Severe allergic reaction"],
        "side_effects": ["Redness"],
        "notes": "Protects against invasive Hib disease."
    },
    {
        "name": "Pneumococcal (PCV13/15/20)",
        "primary_series_doses": 4,
        "price_per_dose": 55.0,
        "administration_route": "IM",
        "age_min": 0.17,
        "contraindications": ["Severe allergic reaction"],
        "side_effects": ["Fever", "Irritability"],
        "notes": "Conjugate vaccine; adult risk-based revaccination varies."
    },
    {
        "name": "Rotavirus (Monovalent)",
        "primary_series_doses": 2,
        "price_per_dose": 75.0,
        "administration_route": "Oral",
        "age_min": 0.17,
        "age_max": 0.5,
        "contraindications": ["History of intussusception", "Severe SCID"],
        "side_effects": ["Mild diarrhea"],
        "notes": "Complete before 24 weeks of age."
    },
    {
        "name": "Rotavirus (Pentavalent)",
        "primary_series_doses": 3,
        "price_per_dose": 75.0,
        "administration_route": "Oral",
        "age_min": 0.17,
        "age_max": 0.5,
        "contraindications": ["History of intussusception", "Severe SCID"],
        "side_effects": ["Mild diarrhea"],
        "notes": "Alternative formulation."
    },
    {
        "name": "MMR (Measles, Mumps, Rubella)",
        "primary_series_doses": 2,
        "price_per_dose": 25.0,
        "administration_route": "SC",
        "age_min": 1,
        "contraindications": ["Pregnancy", "Severe immunosuppression"],
        "side_effects": ["Mild rash", "Fever"],
        "notes": "Live attenuated."
    },
    {
        "name": "Varicella (Chickenpox)",
        "primary_series_doses": 2,
        "price_per_dose": 45.0,
        "administration_route": "SC",
        "age_min": 1,
        "contraindications": ["Pregnancy", "Immunosuppression"],
        "side_effects": ["Mild rash"],
        "notes": "Live attenuated."
    },
    {
        "name": "Meningococcal ACWY (Conjugate)",
        "primary_series_doses": 1,
        "booster_interval_years": 5.0,
        "price_per_dose": 60.0,
        "administration_route": "IM",
        "age_min": 0.5,
        "contraindications": ["Severe allergic reaction"],
        "side_effects": ["Soreness"],
        "notes": "Booster for ongoing risk."
    },
    {
        "name": "Meningococcal B",
        "primary_series_doses": 2,
        "price_per_dose": 95.0,
        "administration_route": "IM",
        "age_min": 0.5,
        "contraindications": ["Severe allergic reaction"],
        "side_effects": ["Fever", "Soreness"],
        "notes": "Schedule differs by product."
    },
    {
        "name": "HPV (Human Papillomavirus)",
        "primary_series_doses": 2,
        "price_per_dose": 120.0,
        "administration_route": "IM",
        "age_min": 9,
        "age_max": 45,
        "contraindications": ["Pregnancy"],
        "side_effects": ["Pain", "Redness"],
        "notes": "3 doses if series starts ≥15 years."
    },
    # --- Adolescent / Adult Boosters ---
    {
        "name": "Tdap (Tetanus, Diphtheria, Pertussis)",
        "primary_series_doses": 1,
        "booster_interval_years": 10.0,
        "price_per_dose": 35.0,
        "administration_route": "IM",
        "age_min": 10,
        "contraindications": ["Encephalopathy after pertussis vaccine"],
        "side_effects": ["Soreness", "Fatigue"],
        "notes": "One-time Tdap, then Td/Tdap every 10 years."
    },
    {
        "name": "Td (Tetanus, Diphtheria)",
        "primary_series_doses": None,
        "booster_interval_years": 10.0,
        "price_per_dose": 20.0,
        "administration_route": "IM",
        "age_min": 7,
        "contraindications": ["Severe allergic reaction"],
        "side_effects": ["Soreness"],
        "notes": "Booster maintenance after Tdap."
    },
    # --- Seasonal / Recurring ---
    {
        "name": "Influenza (Inactivated)",
        "primary_series_doses": None,
        "recurrence_interval_years": 1.0,
        "price_per_dose": 20.0,
        "administration_route": "IM",
        "age_min": 0.5,
        "contraindications": ["Severe egg allergy (product dependent)"],
        "side_effects": ["Mild fever", "Fatigue"],
        "notes": "Annual."
    },
    {
        "name": "Influenza (Live Attenuated Nasal)",
        "primary_series_doses": None,
        "recurrence_interval_years": 1.0,
        "price_per_dose": 25.0,
        "administration_route": "IN",
        "age_min": 2,
        "age_max": 49,
        "contraindications": ["Pregnancy", "Immunosuppression", "Asthma <5"],
        "side_effects": ["Runny nose"],
        "notes": "Annual; live attenuated."
    },
    {
        "name": "COVID-19 (mRNA)",
        "primary_series_doses": 2,
        "booster_interval_years": 1.0,
        "price_per_dose": 30.0,
        "administration_route": "IM",
        "age_min": 5,
        "contraindications": ["Severe allergic reaction to component"],
        "side_effects": ["Fatigue", "Fever", "Myalgia"],
        "notes": "Periodic boosters per guidance."
    },
    # --- Travel / Risk-Based ---
    {
        "name": "Yellow Fever",
        "primary_series_doses": 1,
        "price_per_dose": 70.0,
        "administration_route": "SC",
        "age_min": 0.75,
        "contraindications": ["Egg allergy", "Immunosuppression", "Thymus disorder"],
        "side_effects": ["Fever", "Headache"],
        "notes": "Single lifelong dose; certificate for travel."
    },
    {
        "name": "Typhoid (Injectable Vi)",
        "primary_series_doses": 1,
        "recurrence_interval_years": 3.0,
        "price_per_dose": 38.0,
        "administration_route": "IM",
        "age_min": 2,
        "contraindications": ["Severe allergic reaction"],
        "side_effects": ["Fever", "Headache"],
        "notes": "Booster if ongoing exposure."
    },
    {
        "name": "Typhoid (Oral Live)",
        "primary_series_doses": 4,
        "recurrence_interval_years": 5.0,
        "price_per_dose": 12.0,
        "administration_route": "Oral",
        "age_min": 6,
        "contraindications": ["Immunosuppression"],
        "side_effects": ["Mild GI upset"],
        "notes": "4 capsules over 7 days."
    },
    {
        "name": "Rabies (Pre-exposure)",
        "primary_series_doses": 2,
        "booster_interval_years": 3.0,
        "price_per_dose": 74.0,
        "administration_route": "IM",
        "age_min": 0,
        "contraindications": ["Severe allergic reaction"],
        "side_effects": ["Headache", "Nausea"],
        "notes": "Booster for continued high risk."
    },
    {
        "name": "Japanese Encephalitis",
        "primary_series_doses": 2,
        "booster_interval_years": 1.0,
        "price_per_dose": 95.0,
        "administration_route": "IM",
        "age_min": 2,
        "contraindications": ["Severe allergic reaction"],
        "side_effects": ["Headache", "Myalgia"],
        "notes": "Booster if prolonged risk."
    },
    {
        "name": "Cholera (Oral Inactivated)",
        "primary_series_doses": 2,
        "recurrence_interval_years": 2.0,
        "price_per_dose": 35.0,
        "administration_route": "Oral",
        "age_min": 2,
        "contraindications": ["Vomiting within 1 hour (repeat dose)"],
        "side_effects": ["GI discomfort"],
        "notes": "Booster if risk persists."
    },
    {
        "name": "Tick-borne Encephalitis (TBE)",
        "primary_series_doses": 3,
        "booster_interval_years": 5.0,
        "price_per_dose": 60.0,
        "administration_route": "IM",
        "age_min": 1,
        "contraindications": ["Severe allergic reaction"],
        "side_effects": ["Headache", "Fatigue"],
        "notes": "Shorter booster interval for older adults."
    },
    {
        "name": "Hepatitis A",
        "primary_series_doses": 2,
        "price_per_dose": 45.0,
        "administration_route": "IM",
        "age_min": 1,
        "contraindications": ["Severe allergic reaction"],
        "side_effects": ["Headache", "Soreness"],
        "notes": "Second dose 6–18 months later."
    },
    {
        "name": "Hepatitis A + B (Combined)",
        "primary_series_doses": 3,
        "price_per_dose": 60.0,
        "administration_route": "IM",
        "age_min": 1,
        "contraindications": ["Yeast allergy"],
        "side_effects": ["Soreness"],
        "notes": "Accelerated schedules exist."
    },
    {
        "name": "Typhus (Rickettsial) – Placeholder",
        "primary_series_doses": 1,
        "price_per_dose": 0.0,
        "administration_route": "IM",
        "age_min": 5,
        "contraindications": ["Severe allergic reaction"],
        "side_effects": ["Soreness"],
        "notes": "Add real product details if applicable."
    },
    # --- Special Circumstances / Risk Groups ---
    {
        "name": "BCG (Tuberculosis)",
        "primary_series_doses": 1,
        "price_per_dose": 35.0,
        "administration_route": "ID",
        "age_min": 0,
        "contraindications": ["Immunosuppression"],
        "side_effects": ["Local ulcer"],
        "notes": "Given to high-risk infants / occupational risk."
    },
    {
        "name": "Shingles (Recombinant Zoster)",
        "primary_series_doses": 2,
        "price_per_dose": 150.0,
        "administration_route": "IM",
        "age_min": 50,
        "contraindications": ["Severe allergic reaction"],
        "side_effects": ["Fatigue", "Myalgia"],
        "notes": "Second dose 2–6 months later."
    },
    {
        "name": "RSV (Older Adult)",
        "primary_series_doses": 1,
        "price_per_dose": 180.0,
        "administration_route": "IM",
        "age_min": 60,
        "contraindications": ["Severe allergic reaction"],
        "side_effects": ["Fatigue", "Headache"],
        "notes": "Single dose; guidance evolving."
    },
    {
        "name": "RSV (Maternal)",
        "primary_series_doses": 1,
        "price_per_dose": 180.0,
        "administration_route": "IM",
        "age_min": 18,
        "contraindications": ["Severe allergic reaction"],
        "side_effects": ["Fatigue"],
        "notes": "Administer during pregnancy window."
    },
    {
        "name": "Anthrax (Pre-exposure)",
        "primary_series_doses": 5,
        "booster_interval_years": 1.0,
        "price_per_dose": 140.0,
        "administration_route": "IM",
        "age_min": 18,
        "contraindications": ["Severe allergic reaction"],
        "side_effects": ["Injection site reaction"],
        "notes": "Occupational risk groups."
    },
    {
        "name": "Smallpox/Monkeypox (MVA-BN)",
        "primary_series_doses": 2,
        "price_per_dose": 110.0,
        "administration_route": "SC",
        "age_min": 18,
        "contraindications": ["Severe allergic reaction"],
        "side_effects": ["Fatigue", "Headache"],
        "notes": "High-risk / outbreak use."
    },
    # --- STD / Bloodborne (some already above) ---
    {
        "name": "Hepatitis C – (No vaccine; placeholder)",
        "primary_series_doses": None,
        "price_per_dose": 0.0,
        "administration_route": "IM",
        "age_min": 0,
        "contraindications": [],
        "side_effects": [],
        "notes": "No licensed vaccine (placeholder entry if needed)."
    }
]




seed_branches = [
    {
        "name": "West Clock Town Wellness and Curiosity Clinic",
        "address": "18 Main Street, West Clock Town, Termina",
        "postcode": "CT 67912",
        "phone": "01759 389781",
        "email": "maskmedic@clocktownclinic.tm",
        "opening_hours": [
            {"days": "Mon-Sun", "open": "22:00", "close": "06:00"} 
        ],
        "image_url": "img/branches/westclocktown.jpg"
    },
    {
        "name": "Kakariko Village Health Post",
        "address": "Beneath The Well, Kakariko Village, Hyrule",
        "postcode": "KV 45012",
        "phone": "01743 776217",
        "email": "admin@kakarikohealth.hy",
        "opening_hours": [
            {"days": "Sun-Thu", "open": "09:00", "close": "18:00"},
        ],
        "image_url": "img/branches/beneaththewell.jpg"
    },
    {
        "name": "Garo's Apothecary",
        "address": "Stone Tower Atrium, Ikana Canyon, Termina",
        "postcode": "IK 23901",
        "phone": "01904 429767",
        "email": "undeadcare@ikanapharma.tm",
        "opening_hours": [
            {"days": "Mon-Fri", "open": "08:00", "close": "19:00"},
            {"days": "Sat", "open": "09:00", "close": "17:00"},
            {"days": "Sun", "open": "12:00", "close": "17:00"},
        ],
        "image_url": "img/branches/stonetower.jpg"
    },
    {
        "name": "Hyrule Castle Town Potion Shop",
        "address": "16 Royal Avenue, Hyrule Castle Town, Hyrule",
        "postcode": "HC 17843",
        "phone": "020 8709 0001",
        "email": "agatha@hyrulectpotionshop.hy",
        "opening_hours": [
            {"days": "Mon-Fri", "open": "09:00", "close": "20:00"},
            {"days": "Sat-Sun", "open": "10:00", "close": "18:00"},
        ],
        "image_url": "img/branches/backalley.jpg"
    },
    {
        "name": "Cherrygrove City Pokémon Center",
        "address": "15 Seashore Boulevard, Cherrygrove City, Johto",
        "postcode": "CG 52346",
        "phone": "01328 980024",
        "email": "nursejoy@cherrygrovepkmncenter.jo",
        "opening_hours": [
            {"days": "Sun-Mon", "open": "00:00", "close": "23:59"},
        ],
        "image_url": "img/branches/cherrygrove.jpg"
    },
    {
        "name": "Skyport Health Pokémon Center",
        "address": "Unit 18, Liberty Pier, Castelia City, Unova",
        "postcode": "UN 56283",
        "phone": "01876 298312",
        "email": "nursejoy@skyporthealth.un",
        "opening_hours": [
            {"days": "Sun-Mon", "open": "00:00", "close": "23:59"},
        ],
        "image_url": "img/branches/casteliacity.jpg"
    },
]