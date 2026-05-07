import subprocess


def safe_local_name(registry_name: str) -> str:
    return (
        registry_name
        .replace("io.github.", "")
        .replace("com.", "")
        .replace("ai.", "")
        .replace("/", "-")
        .replace(".", "-")
    )


def install_mcp(server: dict) -> tuple[bool, str]:
    s = server["server"]
    registry_name = s["name"]
    local_name = safe_local_name(registry_name)

    remotes = s.get("remotes", [])
    packages = s.get("packages", [])

    if remotes:
        url = remotes[0]["url"]
        cmd = ["claude", "mcp", "add", "--transport", "http", local_name, url]
    elif packages:
        pkg = packages[0]
        registry_type = pkg.get("registryType", "").lower()
        pkg_identifier = pkg.get("identifier", "")

        if not pkg_identifier:
            return False, "package has no identifier field"

        if registry_type == "npm":
            cmd = ["claude", "mcp", "add", local_name, "--", "npx", "-y", pkg_identifier]
        elif registry_type == "pypi":
            cmd = ["claude", "mcp", "add", local_name, "--", "uvx", pkg_identifier]
        elif registry_type == "oci":
            return False, "OCI/Docker registry not supported yet"
        else:
            return False, f"unsupported registryType: '{registry_type}'"
    else:
        return False, "no install metadata (no remotes, no packages)"

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        return False, "install timed out"
    except FileNotFoundError:
        return False, "claude CLI not found in PATH"

    success = result.returncode == 0
    output = result.stderr.strip() or result.stdout.strip()
    return success, output[:300]  # limita output lunghi