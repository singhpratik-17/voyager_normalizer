import json

class VoyagerNormalizer:
    def get_deep(self, data, path, default=None):
        """Safely navigates nested dictionaries using a dot-separated path."""
        keys = path.split('.')
        for key in keys:
            if isinstance(data, dict):
                data = data.get(key)
            else:
                return default
        return data if data is not None else default

    def normalize(self, raw_data):
        """Maps messy JSON to a clean Canonical format."""
        urn = self.get_deep(raw_data, "profile.entityUrn", "")
        clean_id = urn.split(":")[-1] if urn else None

        return {
            "id": clean_id,
            "full_name": f"{self.get_deep(raw_data, 'profile.firstName', '')} {self.get_deep(raw_data, 'profile.lastName', '')}".strip(),
            "headline": self.get_deep(raw_data, "profile.headline"),
            "experience": self._extract_exp(raw_data)
        }

    def _extract_exp(self, data):
        elements = self.get_deep(data, "positions.elements", [])
        return [{"title": e.get("title"), "company": e.get("companyName")} for e in elements]

if __name__ == "__main__":
    with open("raw_voyager.json", "r") as f:
        raw = json.load(f)
    print(json.dumps(VoyagerNormalizer().normalize(raw), indent=2))