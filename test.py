import re
from pdfminer.high_level import extract_text

def extract_specific_pages_from_pdf_with_pdfminer(pdf_path, page_numbers):
    """
    Extract text from specific pages of a PDF using pdfminer.
    """
    text = ""
    for page_num in page_numbers:
        text += extract_text(pdf_path, page_numbers=[page_num-1])
    return text

def extract_required_details_from_segment(text):
    """
    Extract specific details from the provided text segment.
    """
    details = {}
    
    # Dénomination (Company Name)
    denomination_match = re.search(r"Dénomination\n\nDénomination\n\n(.*?)\n", text)
    if denomination_match:
        details["Dénomination"] = denomination_match.group(1).strip()
    
    # Forme juridique (Legal Form)
    forme_juridique_match = re.search(r"Forme juridique\n\nForme juridique\n\n(.*?)\n", text)
    if forme_juridique_match:
        details["Forme juridique"] = forme_juridique_match.group(1).strip()
    
    # Siège social (Registered Office)
    siege_social_match = re.search(r"Siège social\n\n(.*?)\n\nObjet social", text, re.DOTALL)
    if siege_social_match:
        siege_social = siege_social_match.group(1).replace("\n", " ").strip()
        details["Siège social"] = siege_social
    
    # Objet social (Corporate Purpose)
    objet_social_match = re.search(r"Objet social \(indication\)\n\n(.*?)\n\n✔ Objet social incomplet", text, re.DOTALL)
    if objet_social_match:
        details["Objet social"] = objet_social_match.group(1).replace("\n", " ").strip()
    
    # Capital social (Share Capital)
    capital_social_match = re.search(r"Capital social / Fonds social\n\n.*?Montant\n\n(.*?)\n.*?Devise\n\n(.*?)\n", text, re.DOTALL)
    if capital_social_match:
        details["Capital social"] = capital_social_match.group(1).strip() + " " + capital_social_match.group(2).strip()
    
    return details

def extract_date_constitution_exercice_social(text):
    """
    Extract Date de constitution and Exercice social from the provided text segment.
    """
    details = {}
    
    # Extracting Date de constitution (Date of Incorporation)
    date_constitution_match = re.search(r"Date de constitution\n\nDate de constitution\n\n(.*?)\n", text)
    if date_constitution_match:
        details["Date de constitution"] = date_constitution_match.group(1).strip()
    
    # Extracting Exercice Social (Financial Year)
    exercice_social_match = re.search(r"Exercice social\nPremier exercice ou exercice raccourci\nDu\n(.*?)\nAu\n(.*?)\nExercice social\nDu\n(.*?)\nAu\n(.*?)$", text, re.DOTALL)
    if exercice_social_match:
        details["Exercice Social"] = {
            "Premier exercice ou exercice raccourci": {
                "Start Date": exercice_social_match.group(1).strip(),
                "End Date": exercice_social_match.group(2).strip()
            },
            "Regular Financial Year": {
                "Start Date": exercice_social_match.group(3).strip(),
                "End Date": exercice_social_match.group(4).strip()
            }
        }
    
    return details

def extract_detailed_associates_from_page(text):
    """
    Extract detailed Associé(s) information from the provided text segment.
    """
    details = {}
    
    # Nouvel associé details
    nouvel_associe_details = {
        "Name": re.search(r"Nouvel associé :\s*(.*?)\n", text).group(1).strip(),
        "Type": re.search(r"Type de personne\n\n(.*?)\n", text).group(1).strip(),
        "Date of Birth": re.search(r"Date de naissance\n\n(.*?)\n", text).group(1).strip(),
        "Place of Birth": re.search(r"Lieu de naissance\n(.*?)\n", text).group(1).strip(),
        "Address": {
            "Street": re.search(r"Rue \(.*?\)\n\n(.*?)\n", text).group(1).strip(),
            "Number": re.search(r"Numéro\n\n(.*?)\n", text).group(1).strip(),
            "Postal Code": re.search(r"Code postal\n\n(.*?)\n", text).group(1).strip(),
            "City": re.search(r"Localité\n\n(.*?)\n", text).group(1).strip(),
            "Country": re.search(r"Pays\n\n(.*?)\n", text).group(1).strip()
        },
        "Shares": re.search(r"Parts sociales\n\n(.*?)\n", text).group(1).strip(),
        "Total Shares Held": re.search(r"Nombre de parts détenues\n\n(.*?)\n", text).group(1).strip()
    }
    
    details["Nouvel associé Details"] = nouvel_associe_details
    
    return details

# Example usage:
pdf_path = "path_to_your_pdf"
pdf_content = extract_specific_pages_from_pdf_with_pdfminer(pdf_path, list(range(4, 9)))
details = {}
details.update(extract_required_details_from_segment(pdf_content))
details.update(extract_date_constitution_exercice_social(pdf_content))
details.update(extract_detailed_associates_from_page(pdf_content))

print(details)




import re

def extract_information_from_pdf(text):
    structured_data = {
        "Dénomination": re.search(r"Dénomination\n\nLuxoland S\.à r\.l\.-S\.", text).group(0).split("\n\n")[1],
        "Forme juridique": re.search(r"Forme juridique\n\nSociété à responsabilité limitée simplifiée", text).group(0).split("\n\n")[1],
        "Siège social": {
            "Numéro": re.search(r"Siège social\n\nNuméro\n\n([^\n]+)", text).group(1),
            "Rue": re.search(r"Theinshaff", text).group(0),
            "Code postal": re.search(r"7634", text).group(0),
            "Localité": re.search(r"7634\n\n([^\n]+)", text).group(1)
        },
        "Objet social": re.search(r"La société a pour objet .* réalisation\.", text, re.DOTALL).group(0),
        "Capital social": {
            "Montant": re.search(r"Montant\n\n([^\n]+)", text).group(1),
            "Devise": re.search(r"Devise\n\n([^\n]+)", text).group(1)
        },
        "Date de constitution": re.search(r"Date de constitution\n\n(\d{2}/\d{2}/\d{4})", text).group(1),
        "Associé": {
            "Nom": re.search(r"Nouvel associé :\n([^\n]+)", text).group(1),
            "Type de personne": re.search(r"Type de personne\n\n([^\n]+)", text).group(1),
            "Date de naissance": re.search(r"Date de naissance\n\n([^\n]+)", text).group(1),
            "Lieu de naissance": re.search(r"Lieu de naissance\n([^\n]+)", text).group(1),
            "Adresse": {
                "Numéro": re.findall(r"Numéro\n\n([^\n]+)", text)[1],
                "Rue": re.findall(r"Rue \(.*\)\n\n([^\n]+)", text)[1],
                "Code postal": re.findall(r"7634", text)[1],
                "Localité": re.findall(r"7634\n\n([^\n]+)", text)[1]
            }
        },
        "Administrateur/Gérant": {
            "Nom": re.search(r"Nouvel administrateur \/ gérant :\n([^\n]+)", text).group(1),
            "Type de personne": re.findall(r"Type de personne\n\n([^\n]+)", text)[1],
            "Date de naissance": re.findall(r"Date de naissance\n\n([^\n]+)", text)[1],
            "Lieu de naissance": re.findall(r"Lieu de naissance\n([^\n]+)", text)[1],
            "Adresse": {
                "Numéro": re.findall(r"Numéro\n\n([^\n]+)", text)[2],
                "Rue": re.findall(r"Rue \(.*\)\n\n([^\n]+)", text)[2],
                "Code postal": re.findall(r"7634", text)[2],
                "Localité": re.findall(r"7634\n\n([^\n]+)", text)[2]
            },
            "Fonction": re.search(r"Fonction\n\n([^\n]+)", text).group(1),
            "Date de nomination": re.search(r"Date de nomination\n\n([^\n]+)", text).group(1)
        }
    }
    return structured_data
