#!/usr/bin/env python
"""Runs after cookiecutter generates the project."""
import subprocess
import sys
import os
import glob
import platform
import secrets

# These values are substituted by Jinja2 when cookiecutter renders this hook.
PROJECT_SLUG  = "{{cookiecutter.project_slug}}"
PRIMARY_COLOR = "{{cookiecutter.primary_color}}"
SITE_NAME     = "{{cookiecutter.site_name}}"
AUTHOR_EMAIL  = "{{cookiecutter.author_email}}"


# ---------------------------------------------------------------------------
# Step 1: replace template placeholders in .py / .css files
# (those extensions are in _copy_without_render so Jinja2 skipped them)
# ---------------------------------------------------------------------------
REPLACEMENTS = {
    "__PROJECT_SLUG__": PROJECT_SLUG,
    "__PRIMARY_COLOR__": PRIMARY_COLOR,
}

def substitute_placeholders():
    for pattern in ("**/*.py", "styling/**/*.css"):
        for filepath in glob.glob(pattern, recursive=True):
            try:
                with open(filepath, encoding="utf-8") as f:
                    content = f.read()
                new = content
                for placeholder, value in REPLACEMENTS.items():
                    new = new.replace(placeholder, value)
                if new != content:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(new)
            except (UnicodeDecodeError, PermissionError):
                pass


def run(cmd, **kwargs):
    print(f"  $ {' '.join(str(c) for c in cmd)}")
    result = subprocess.run(cmd, **kwargs)
    if result.returncode != 0:
        print(f"  ERROR: command failed (exit {result.returncode})")
        sys.exit(result.returncode)


def main():
    print("\n🔧 Setting up your project...\n")

    print("🔄 Substituting project name in source files...")
    substitute_placeholders()

    # 2. Install Python dependencies
    print("📦 Installing Python dependencies...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
    )
    if result.returncode != 0:
        print("  Warning: some packages failed to install. Check requirements.txt.")

    # 3. Run migrations
    print("\n🗄️  Running database migrations...")
    run([sys.executable, "manage.py", "migrate"])

    # 4. Load initial SiteConfig fixture
    print("\n🌱 Loading initial site configuration...")
    run([sys.executable, "manage.py", "loaddata", "fixtures/initial.json"])

    # 5. Download Tailwind binary if not present
    tailwind_bin = os.path.join("bin", "tailwindcss")
    if platform.system() == "Windows":
        tailwind_bin += ".exe"

    if not os.path.exists(tailwind_bin):
        print("\n🎨 Downloading Tailwind CSS standalone CLI...")
        system = platform.system().lower()
        arch   = "x64" if platform.machine() in ("x86_64", "AMD64") else "arm64"
        if system == "darwin":
            url = f"https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-macos-{arch}"
        elif system == "linux":
            url = f"https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-{arch}"
        else:
            url = f"https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-windows-{arch}.exe"

        os.makedirs("bin", exist_ok=True)
        try:
            import urllib.request
            urllib.request.urlretrieve(url, tailwind_bin)
            os.chmod(tailwind_bin, 0o755)
        except Exception as e:
            print(f"  Warning: could not download Tailwind: {e}")
            print("  Run manually: https://tailwindcss.com/blog/standalone-cli")

    # 6. Compile Tailwind
    if os.path.exists(tailwind_bin):
        print("\n🎨 Compiling Tailwind CSS...")
        run([
            tailwind_bin,
            "-i", "styling/static_src/input.css",
            "-o", "templates/css/output.css",
            "--minify",
        ])

    # 7. Generate .env
    if not os.path.exists(".env"):
        print("\n🔑 Creating .env file...")
        with open(".env", "w") as f:
            f.write(f"SECRET_KEY={secrets.token_urlsafe(50)}\n")
            f.write("DEBUG=True\n")
            f.write("ALLOWED_HOSTS=localhost,127.0.0.1\n")

    print(f"""
✅ Project ready!

Next steps:
  python manage.py createsuperuser
  python manage.py runserver

Then visit http://127.0.0.1:8000/admin/ to configure your site.
""")


if __name__ == "__main__":
    main()
