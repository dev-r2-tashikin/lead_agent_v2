**Agent_Website_Info Tasks:**
1.  **Phase 1: 确立并验证锚点 (Anchor Identification & Validation)**
    *   SET `Official_Website_URL` = `null`
    *   ITERATE through URLs in order of priority: Category 1 -> Category 3 -> Category 2 -> Category 5 -> Category 7.
        *   URL: `https://chestpain-analyzer.com/` (Category 1)
            *   子任务：相关性检查: CHECK HTML content for "K-MARA Healthcare Corporation".
            *   IF `相关性检查` == TRUE:
                *   EXTRACT `https://chestpain-analyzer.com/` as a potential official website.
                *   SET `Official_Website_URL` = `https://chestpain-analyzer.com/`
                *   GOTO Phase 2A.
2.  **Phase 2A: 核心刮取 (Core Scraping) - 官网深度刮取**
    *   VISIT `Official_Website_URL` (`https://chestpain-analyzer.com/`)
    *   EXTRACT contact information (email, phone number) from `Official_Website_URL` using regex for email patterns (`[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}`) and phone numbers (`\+\d{1,3}\s?\d{1,4}\s?\d{4,10}`).
    *   VISIT `Official_Website_URL` + `/product-information` (`https://chestpain-analyzer.com/product-information`)
    *   EXTRACT product lines/descriptions related to Chest Pain Analyzer.
    *   VISIT `Official_Website_URL` + `/privacy-policy` (`https://chestpain-analyzer.com/privacy-policy`)
    *   EXTRACT legal name of the entity owning the website (e.g., "K-MARA Healthcare Corporation SRL").
    *   VISIT `Official_Website_URL` + `/where-you-can-buy` (`https://chestpain-analyzer.com/where-you-can-buy`)
    *   EXTRACT partner/distributor names mentioned on this page (e.g., "Biopanda Reagents").
    *   VISIT `Official_Website_URL` + `/k-mara-chest-pain-analyzer` (`https://chestpain-analyzer.com/k-mara-chest-pain-analyzer`)
    *   EXTRACT detailed product information.
    *   SCAN `Official_Website_URL` and its sub-pages (e.g., `/product-information`, `/about`) for keywords: "distributor", "reseller", "partner".
    *   IF "distributor" OR "reseller" OR "partner" keywords are found within the `Official_Website_URL` domain, THEN SET `Is_Distributor` = TRUE. ELSE SET `Is_Distributor` = FALSE.
    *   VISIT `https://kmaramedical.ro/en/` (Category 1)
    *   子任务：相关性检查: CHECK HTML content for "K-MARA Healthcare Corporation".
    *   IF `相关性检查` == TRUE:
        *   EXTRACT contact information (email, phone number) from `https://kmaramedical.ro/en/` and its sub-pages like `/contact-us/`.
        *   EXTRACT product lines/descriptions from `https://kmaramedical.ro/en/products/` and `https://kmaramedical.ro/en/product/fluorescence-immunoassay-analyser-fia-ivd-reader/`, `https://kmaramedical.ro/en/rapid-tests-non-medical/`.
        *   EXTRACT legal information and authorization details from PDFs: `https://storage.e.jimdo.com/file/b6e1d10e-e12a-4419-a1e2-6e8680280180/RECOMMEDE+PRODUCT+LIST+2024+FINAL.pdf`, `https://storage.e.jimdo.com/file/0f26455b-9ad3-4b52-a1b9-e2b1c4e9edb3/EN_K-MARA_RO_151023.pdf`, `https://storage.e.jimdo.com/file/3ed07c4c-e826-4ebb-99a9-4bd14f3c9352/RO_TesteRapideUzUman_23.pdf`, `https://jimdo-storage.freetls.fastly.net/file/43b30ed5-2e03-4317-897c-0a196c7b745b/RO_Teste_Elisa_Food.pdf`, `https://storage.e.jimdo.com/file/f62954de-fffb-4569-bf23-7b0e3e67cd45/RO_TesteRapideVeterinare+23.pdf`, `https://kmaramedical.ro/wp-content/uploads/2024/03/EN__Authorization_K-MARA_-Healthcare-Corporation_19.10.2023.pdf`, `https://kmaramedical.ro/wp-content/uploads/2024/02/RO_Autorizatie_K-MARA_-Healthcare-Corporation_19.10.2023.pdf`.
        *   SCAN these URLs for keywords: "distributor", "reseller", "partner". Update `Is_Distributor` if found.
    *   VISIT `https://www.kmarahealthcare.com/` (Category 1)
    *   子任务：相关性检查: CHECK HTML content for "K-MARA Healthcare Corporation".
    *   IF `相关性检查` == TRUE:
        *   EXTRACT contact information, products, and general company information from its sub-pages like `/about-us/germany/`, `/about-us/france/`, `/delivery-policy/`, `/support-and-news/romania/`, `/support-and-news/`.
        *   SCAN for keywords: "distributor", "reseller", "partner". Update `Is_Distributor` if found.
    *   VISIT `https://kmaraconfigurator.jimdofree.com/about/` (Category 1)
    *   子任务：相关性检查: CHECK HTML content for "K-MARA Healthcare Corporation".
    *   IF `相关性检查` == TRUE:
        *   EXTRACT information about the healthcare group.
        *   SCAN for keywords: "distributor", "reseller", "partner". Update `Is_Distributor` if found.
    *   VISIT `https://www.kmarahealthline.com/` (Category 1)
    *   子任务：相关性检查: CHECK HTML content for "K-MARA Healthcare Corporation".
    *   IF `相关性检查` == TRUE:
        *   EXTRACT any available information.
        *   SCAN for keywords: "distributor", "reseller", "partner". Update `Is_Distributor` if found.
    *   VISIT `https://kmaradefense.jimdofree.com/k-mara-products/` (Category 1)
    *   子任务：相关性检查: CHECK HTML content for "K-MARA Healthcare Corporation".
    *   IF `相关性检查` == TRUE:
        *   EXTRACT information about defense/partner products.
        *   SCAN for keywords: "distributor", "reseller", "partner". Update `Is_Distributor` if found.
    *   VISIT `https://www.chest-pain-analyzing.org/` (Category 1)
    *   子任务：相关性检查: CHECK HTML content for "K-MARA Healthcare Corporation".
    *   IF `相关性检查` == TRUE:
        *   EXTRACT information about their quick tests.
        *   SCAN for keywords: "distributor", "reseller", "partner". Update `Is_Distributor` if found.
    *   VISIT `https://kmara-support.jimdofree.com/` (Category 1)
    *   子任务：相关性检查: CHECK HTML content for "K-MARA Healthcare Corporation".
    *   IF `相关性检查` == TRUE:
        *   EXTRACT information about support and partnerships.
        *   SCAN for keywords: "distributor", "reseller", "partner". Update `Is_Distributor` if found.
    *   VISIT `https://kmara-cruise.jimdofree.com/` (Category 1)
    *   子任务：相关性检查: CHECK HTML content for "K-MARA Healthcare Corporation".
    *   IF `相关性检查` == TRUE:
        *   EXTRACT information about the cruise healthcare division.
        *   SCAN for keywords: "distributor", "reseller", "partner". Update `Is_Distributor` if found.
    *   ITERATE through Category 6 URLs:
        *   URL: `https://en.wikipedia.org/wiki/ISO_13485`
            *   子任务：相关性检查: CHECK HTML content for "K-MARA Healthcare Corporation".
            *   IF `相关性检查` == TRUE: (Unlikely, but for completeness) EXTRACT relevance to K-MARA.
        *   URL: `https://www.iso.org/iso-13485-medical-devices.html`
            *   子任务：相关性检查: CHECK HTML content for "K-MARA Healthcare Corporation".
            *   IF `相关性检查` == TRUE: EXTRACT relevance to K-MARA.
        *   URL: `https://www.nqa.com/en-us/certification/standards/iso-13485`
            *   子任务：相关性检查: CHECK HTML content for "K-MARA Healthcare Corporation".
            *   IF `相关性检查` == TRUE: EXTRACT relevance to K-MARA.

**Agent_People_Info Tasks:**
1.  **Phase 2B: 核心刮取与关系判定 (Core Scraping & Role Definition) - 第三方关系判定 (People Focused)**
    *   VISIT `https://www.linkedin.com/company/k-mara-healthcare-corporation` (Category 1)
    *   子任务：相关性检查: CHECK page content for "K-MARA Healthcare Corporation".
    *   IF `相关性检查` == TRUE:
        *   EXTRACT company description, employee count, primary industry.
    *   VISIT `https://ro.linkedin.com/company/k-mara-healthcare-corporation` (Category 1)
    *   子任务：相关性检查: CHECK page content for "K-MARA Healthcare Corporation".
    *   IF `相关性检查` == TRUE:
        *   EXTRACT company description, employee count, primary industry specific to Romania.
    *   VISIT `https://www.linkedin.com/company/pharmact-healthcare` (Category 1)
    *   子任务：相关性检查: CHECK page content for "K-MARA HEALTHCARE S.L.".
    *   IF `相关性检查` == TRUE:
        *   EXTRACT company description and employee count.
    *   VISIT `https://ro.linkedin.com/in/rolfpetermilczarek-a58a5752/en` (Category 3)
    *   子任务：相关性检查: CHECK HTML content for "K-MARA Healthcare Corporation".
    *   IF `相关性检查` == TRUE:
        *   EXTRACT job title and company affiliation.
        *   SET `Rolf_Peter_Title` = "Chief Operating Officer, K-MARA Healthcare Corporation".
    *   VISIT `https://contactout.com/rolfpeter-m-75228` (Category 3)
    *   子任务：相关性检查: CHECK HTML content for "K-MARA Healthcare Corporation".
    *   IF `相关性检查` == TRUE:
        *   EXTRACT email and phone number for Rolfpeter M.
    *   VISIT `https://ro.linkedin.com/in/carmenszasz/en` (Category 3)
    *   子任务：相关性检查: CHECK HTML content for "K-MARA Healthcare Corporation".
    *   IF `相关性检查` == TRUE:
        *   EXTRACT job title and company affiliation.
        *   SET `Carmen_Szasz_Title` = "CEO & Managing Director, K-MARA Healthcare Corporation".
    *   VISIT `https://www.signalhire.com/companies/k-mara-healthcare-corporation` (Category 3)
    *   子任务：相关性检查: CHECK HTML content for "K-MARA Healthcare Corporation".
    *   IF `相关性检查` == TRUE:
        *   EXTRACT any available key personnel names and titles.
    *   VISIT `https://fr.linkedin.com/company/ampulsconsulting?trk=similar-pages_result-card_full-click` (Category 3)
    *   子任务：相关性检查: CHECK HTML content for "K-MARA Healthcare Corporation".
    *   IF `相关性检查` == TRUE:
        *   EXTRACT any mentions of K-MARA and associated roles/industries.
    *   VISIT `https://ch.linkedin.com/company/sanispaces` (Category 3)
    *   子任务：相关性检查: CHECK HTML content for "K-MARA Healthcare Corporation".
    *   IF `相关性检查` == TRUE:
        *   EXTRACT any mentions of K-MARA and associated roles/industries.
    *   VISIT `https://dk.linkedin.com/company/sanispaces` (Category 3)
    *   子任务：相关性检查: CHECK HTML content for "K-MARA Healthcare Corporation".
    *   IF `相关性检查` == TRUE:
        *   EXTRACT any mentions of K-MARA and associated roles/industries.
    *   VISIT `https://uk.linkedin.com/company/sanispaces?trk=public_profile_experience-item_profile-section-card_subtitle-click` (Category 3)
    *   子任务：相关性检查: CHECK HTML content for "K-MARA Healthcare Corporation".
    *   IF `相关性检查` == TRUE:
        *   EXTRACT any mentions of K-MARA and associated roles/industries.
    *   VISIT `https://www.linkedin.com/company/ampulsconsulting` (Category 3)
    *   子任务：相关性检查: CHECK HTML content for "K-MARA Healthcare Corporation".
    *   IF `相关性检查` == TRUE:
        *   EXTRACT any mentions of K-MARA and associated roles/industries.
2.  **Phase 3: 情报增强 (Intelligence Augmentation) - Recruitment Data**
    *   SET `Target_Job_Titles` = []
    *   VISIT `https://eudrugscreening.com/karrier` (Category 8)
    *   子任务：相关性检查: CHECK HTML content for "K-MARA Healthcare Corporation".
    *   IF `相关性检查` == TRUE:
        *   EXTRACT listed job titles.
        *   ADD extracted job titles to `Target_Job_Titles` list.

**Agent_Market_Info Tasks:**
1.  **Phase 2B: 核心刮取与关系判定 (Core Scraping & Role Definition) - 第三方关系判定 (Partnerships and External Mentions)**
    *   SET `Potential_Partner_URLs_List` = []
    *   VISIT `https://eudrugscreening.com/rapid-drug-detection-tests-2` (Category 1)
    *   子任务：相关性检查: CHECK HTML content for "K-MARA Healthcare Corporation".
    *   IF `相关性检查` == TRUE:
        *   SCAN HTML content for "K-MARA Healthcare Corporation" AND ("distributor" OR "partner").
        *   IF found, THEN ADD `https://eudrugscreening.com/rapid-drug-detection-tests-2` to `Potential_Partner_URLs_List`.
    *   VISIT `https://jobselection.ro/en/drug-free-workplaces/` (Category 1)
    *   子任务：相关性检查: CHECK HTML content for "K-MARA Healthcare Corporation".
    *   IF `相关性检查` == TRUE:
        *   SCAN HTML content for "K-MARA Healthcare Corporation" AND ("strategic partnership").
        *   IF found, THEN ADD `https://jobselection.ro/en/drug-free-workplaces/` to `Potential_Partner_URLs_List`.
    *   VISIT `https://kmaradefense.jimdofree.com/k-mara-products/` (Category 1)
    *   子任务：相关性检查: CHECK HTML content for "K-MARA Healthcare Corporation".
    *   IF `相关性检查` == TRUE:
        *   SCAN HTML content for "MANUFACTURER FOR K-MARA. BIOPANDA REAGENTS LTD. UK, based in Belfast, is the exclusive".
        *   IF found, THEN ADD `https://kmaradefense.jimdofree.com/k-mara-products/` to `Potential_Partner_URLs_List`.
2.  **Phase 3: 情报增强 (Intelligence Augmentation) - News and Activities**
    *   SET `Recent_Activities_List` = []
    *   VISIT `https://www.scribd.com/document/691850055/Medicamentele-si-condusul-care-sunt-riscurile` (Category 7)
    *   子任务：相关性检查: CHECK HTML/PDF content for "K-MARA Healthcare Corporation".
    *   IF `相关性检查` == TRUE:
        *   EXTRACT news/event context (e.g., "K-MARA Healthcare Corporation Romania presented by Carmen Szasz").
        *   ADD extracted information to `Recent_Activities_List`.
    *   VISIT `https://www.facebook.com/ColegiulFarmacistilorBrasov/` (Category 7)
    *   子任务：相关性检查: CHECK page content for "K-MARA Healthcare Corporation".
    *   IF `相关性检查` == TRUE:
        *   EXTRACT news/event context (e.g., "K-MARA Healthcare Corporation Romania and Carmen Szasz at an event").
        *   ADD extracted information to `Recent_Activities_List`.
    *   VISIT `https://www.kmjournal.net/news/articleView.html?idxno=2792` (Category 7)
    *   子任务：相关性检查: CHECK HTML content for "K-MARA Healthcare Corporation".
    *   IF `相关性检查` == TRUE:
        *   EXTRACT news/event context (e.g., "CPHI Korea·Hi Korea 2025" and any mention of K-MARA).
        *   ADD extracted information to `Recent_Activities_List`.
    *   ... (Process other relevant Category 7 URLs like `https://www.bloomberg.com/news/articles/2025-08-12/php-pips-kkr-in-battle-to-buy-uk-health-care-landlord-assura` or `https://www.corumgroup.com/insights/growing-healthtech-ma-market` if they explicitly mention K-MARA Healthcare Corporation)
3.  **Phase 4: 系统扩展与归档 (System Scaling & Archiving)**
    *   SET `Global_Task_Queue` = []
    *   ITERATE through Category 4 URLs (Competitors):
        *   URL: `https://karmahealthcare.in/`
            *   EXTRACT company name "Karma Primary Healthcare".
            *   ADD "Karma Primary Healthcare" to `Global_Task_Queue`.
        *   URL: `https://www.gehealthcare.com/`
            *   EXTRACT company name "GE HealthCare".
            *   ADD "GE HealthCare" to `Global_Task_Queue`.
        *   ... (Continue for all Category 4 URLs, adding extracted company names to `Global_Task_Queue`).
    *   ITERATE through Category 5 URLs (Industry Events):
        *   URL: `https://www.medica-tradefair.com/`
            *   EXTRACT event name "MEDICA Trade Fair".
            *   ADD "MEDICA Trade Fair" to `Global_Task_Queue` (for potential future exhibitor list extraction).
        *   URL: `https://www.fimeshow.com/en/exhibitor-list.html`
            *   EXTRACT event name "FIME Medical Exhibition" and company names from exhibitor list.
            *   ADD extracted company names to `Global_Task_Queue`.
        *   ... (Continue for all Category 5 URLs, extracting event names and participant companies to `Global_Task_Queue`).
    *   ITERATE through Category 2 URLs (Corporate Registration & Financial Data):
        *   URL: `https://rocketreach.co/k-mara-healthcare-corporation-email-format_b6ef48d5c6f44c79`
            *   MARK `https://rocketreach.co/k-mara-healthcare-corporation-email-format_b6ef48d5c6f44c79` as `'Verification_Source'`.
            *   ARCHIVE `https://rocketreach.co/k-mara-healthcare-corporation-email-format_b6ef48d5c6f44c79`.
        *   URL: `https://tracxn.com/d/companies/kmara-healthcare/__oOCVyKhj9z86aR0roekt5O86aB7rF9DGC-dnbJCfLU0`
            *   MARK `https://tracxn.com/d/companies/kmara-healthcare/__oOCVyKhj9z86aR0roekt5O86aB7rF9DGC-dnbJCfLU0` as `'Verification_Source'`.
            *   ARCHIVE `https://tracxn.com/d/companies/kmara-healthcare/__oOCVyKhj9z86aR0roekt5O86aB7rF9DGC-dnbJCfLU0`.
        *   ... (Continue for all Category 2 URLs, marking and archiving them).