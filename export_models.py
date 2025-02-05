import os
import django
from django.apps import apps

# Setup Django
# Change to your actual project name
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mp_api.settings")
django.setup()

# Define the output file path
file_path = "models_dump.txt"

# Open the file to write
with open(file_path, "w") as f:
    f.write("📜 Django Models Dump\n\n")

    # Loop through all installed apps
    for app_config in apps.get_app_configs():
        f.write(f"🔹 App: {app_config.label}\n")

        # Loop through all models in the app
        for model in app_config.get_models():
            f.write(f"  - Model: {model.__name__}\n")
            f.write("    Fields:\n")

            # Get each field in the model
            for field in model._meta.fields:
                f.write(
                    f"      - {field.name} ({field.get_internal_type()})\n")

            f.write("\n")  # Space between models

        f.write("\n")  # Space between apps

# Print completion message
print(f"✅ Models exported to {file_path}")
