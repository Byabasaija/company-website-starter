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


def ensure_uv():
    """Return the uv executable path, installing uv if necessary."""
    try:
        if subprocess.run(["uv", "--version"], capture_output=True).returncode == 0:
            return "uv"
    except FileNotFoundError:
        pass

    print("⚡ uv not found — installing it now...")
    if platform.system() == "Windows":
        subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-c",
             "irm https://astral.sh/uv/install.ps1 | iex"],
            check=True,
        )
    else:
        subprocess.run(
            ["sh", "-c", "curl -LsSf https://astral.sh/uv/install.sh | sh"],
            check=True,
        )

    # uv installs to ~/.local/bin on Linux/Mac
    for candidate in [
        os.path.expanduser("~/.local/bin/uv"),
        os.path.expanduser("~/.cargo/bin/uv"),
    ]:
        if os.path.exists(candidate):
            return candidate

    return "uv"


def main():
    print("\n🔧 Setting up your project...\n")

    print("🔄 Substituting project name in source files...")
    substitute_placeholders()

    uv = ensure_uv()

    if platform.system() == "Windows":
        venv_python = os.path.join(".venv", "Scripts", "python.exe")
    else:
        venv_python = os.path.join(".venv", "bin", "python")

    # 1. Create virtual environment
    print("\n🐍 Creating virtual environment...")
    run([uv, "venv", ".venv"])

    # 2. Install Python dependencies
    print("\n📦 Installing Python dependencies...")
    run([uv, "pip", "install", "-r", "requirements.txt", "--python", venv_python])

    # 3. Run migrations
    print("\n🗄️  Running database migrations...")
    run([venv_python, "manage.py", "migrate"])

    # 4. Load initial SiteConfig fixture
    print("\n🌱 Loading initial site configuration...")
    run([venv_python, "manage.py", "loaddata", "fixtures/initial.json"])

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

    # 7. Generate .env.local (used by development settings)
    if not os.path.exists(".env.local"):
        print("\n🔑 Creating .env.local file...")
        with open(".env.local", "w") as f:
            f.write(f"SECRET_KEY={secrets.token_urlsafe(50)}\n")
            f.write("DATABASE_URL=postgres://localhost/{{cookiecutter.project_slug}}\n")

    print(f"""
✅ Project ready!

Next steps:
  source .venv/bin/activate
  python manage.py createsuperuser
  python manage.py runserver

Then visit http://127.0.0.1:8000/admin/ to configure your site.
""")


if __name__ == "__main__":
    main()
