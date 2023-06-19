# This script outputs a entire list of ruleset rules to json files for easy viewing in the "output folder". 
# Add auth-key, auth-email, zone-id.  
# To run: python3 rules.py

import requests
import json
import os
import subprocess

# Check if requests library is installed, install it if not
try:
    import requests
except ImportError:
    print("Requests library not found, installing now...")
    subprocess.check_call(["python", '-m', 'pip', 'install', 'requests'])

# Prompt user for zone ID, email, and API key
AUTH_KEY="<>"
AUTH_EMAIL="<>"
ZONE_ID="<>"

# Set API endpoint URLs
list_rulesets_url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/rulesets"
get_ruleset_url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/rulesets/"

# Make API call to list rulesets
response = requests.get(list_rulesets_url, headers={"X-Auth-Email":AUTH_EMAIL, "X-Auth-Key":AUTH_KEY})

# Parse the JSON response and store ruleset IDs in an array
ruleset_ids = []
for ruleset in response.json()["result"]:
    ruleset_ids.append(ruleset["id"])

# Loop through each ruleset ID and make API call to get ruleset details
for ruleset_id in ruleset_ids:
    response = requests.get(get_ruleset_url + ruleset_id, headers={"X-Auth-Email": AUTH_EMAIL, "X-Auth-Key": AUTH_KEY})
    result = response.json()["result"]

    # Check if result is None
    if result is not None:
        # Create new file in output folder with ruleset name as filename and store response body
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        with open(f"{output_dir}/{result['name']}.json", "w") as f:
            json.dump(result, f)

# Print completion message to screen
print("Complete! Check the output folder for JSON files.")
