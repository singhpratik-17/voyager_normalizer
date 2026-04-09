import json
import os

class VoyagerNormalizer:
    def clean(self, value):
        """Rule: Trim, collapse whitespace, and convert null to empty string."""
        if value is None:
            return ""
        # Collapse multiple spaces into one and strip
        return " ".join(str(value).split())

    def normalize(self, raw):
        # 1. Basic Identity & URL Building
        pub_id = self.clean(raw.get("public_identifier"))
        ln_url = self.clean(raw.get("linkedin_url"))
        if not ln_url and pub_id:
            ln_url = f"https://www.linkedin.com/in/{pub_id}/"

        # 2. Name Derivation Logic
        first = self.clean(raw.get("first_name"))
        last = self.clean(raw.get("last_name"))
        full = self.clean(raw.get("full_name"))

        if full and not (first or last):
            parts = full.split(maxsplit=1)
            first = parts[0] if len(parts) > 0 else ""
            last = parts[1] if len(parts) > 1 else ""
        elif not full:
            full = f"{first} {last}".strip()

        # 3. Positions & Current Role Logic
        raw_positions = raw.get("positions") or []
        normalized_positions = []
        current_role = ""
        current_company = ""

        for pos in raw_positions:
            p_title = self.clean(pos.get("title"))
            p_company = self.clean(pos.get("company_name"))
            p_loc = self.clean(pos.get("location"))
            
            normalized_positions.append({
                "title": p_title,
                "company_name": p_company,
                "location": p_loc
            })

            # Rule: Current if date_range.end is missing/null
            dr = pos.get("date_range") or {}
            if not current_role and (not dr or dr.get("end") is None):
                current_role = p_title
                current_company = p_company

        # 4. Education
        raw_edu = raw.get("educations") or []
        normalized_edu = [
            {
                "school_name": self.clean(e.get("school_name")),
                "degree_name": self.clean(e.get("degree_name")),
                "field_of_study": self.clean(e.get("field_of_study"))
            } for e in raw_edu
        ]

        # 5. Profile Text Generation (Lowercase concat)
        summary = self.clean(raw.get("summary"))
        headline = self.clean(raw.get("headline"))
        loc_name = self.clean(raw.get("location_name"))
        
        text_parts = [headline, summary, loc_name]
        for p in normalized_positions:
            text_parts.extend([p["title"], p["company_name"], p["location"]])
        for e in normalized_edu:
            text_parts.extend([e["school_name"], e["degree_name"], e["field_of_study"]])
        
        profile_text = " ".join([t for t in text_parts if t]).lower()

        return {
            "public_identifier": pub_id,
            "linkedin_url": ln_url,
            "first_name": first,
            "last_name": last,
            "full_name": full,
            "headline": headline,
            "current_role_title": current_role,
            "company_name": current_company,
            "location_name": loc_name,
            "summary": summary,
            "positions": normalized_positions,
            "educations": normalized_edu,
            "profile_text": profile_text
        }

if __name__ == "__main__":
    norm = VoyagerNormalizer()
    
    # Process all JSON files in the current directory
    for filename in os.listdir('.'):
        if filename.endswith('.json') and filename != 'package.json':
            with open(filename, 'r') as f:
                try:
                    raw_data = json.load(f)
                    normalized = norm.normalize(raw_data)
                    print(f"--- Normalized: {filename} ---")
                    print(json.dumps(normalized, indent=2))
                except Exception as e:
                    print(f"Error processing {filename}: {e}")