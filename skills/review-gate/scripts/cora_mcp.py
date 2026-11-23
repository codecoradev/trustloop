#!/usr/bin/env python3
"""Call Cora's MCP tools from the shell when the agent harness has no `cora` MCP server registered
(for example a session that started before `cora install`, or a cloud session that cannot add servers).

It starts `cora mcp` over stdio, calls one tool, prints the tool's text result, and exits.
The same tools and the same verdict store are used as with a registered server.

Usage:
  cora_mcp.py list
  cora_mcp.py call <tool> '<json-arguments>'
  cora_mcp.py prepare <diff-file> [--compact] [--skip-system-prompt]   # cora.review_prepare
  cora_mcp.py finalize <diff-file> <issues-file>  # cora.review_finalize; issues-file holds a JSON array

--compact prints plain text (no JSON escaping) with only what the reviewer needs: valid files, deterministic
findings, the response schema, the system prompt and the user prompt. --skip-system-prompt (with --compact)
prints only the system prompt's SHA-256 instead of its text: use it from the second review round on, when the
hash matches the one printed in the first round, so the same reviewer instructions are not read twice.

Run it from inside the repository being reviewed (Cora reads the project config and index from the cwd).
Pass the same, unmodified diff file to prepare and finalize: the verdict covers exactly that input.
"""
import json
import os
import shutil
import subprocess
import sys

PROTOCOL = "2025-06-18"


def cora_binary():
    path = os.environ.get("CORA_BIN") or shutil.which("cora")
    if not path:
        sys.exit("cora not found on PATH. Install the release binary: "
                 "curl -fsSL https://raw.githubusercontent.com/codecoradev/cora-code/main/install.sh | sh")
    return path


class Session:
    def __init__(self):
        self.proc = subprocess.Popen([cora_binary(), "mcp"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                     stderr=subprocess.DEVNULL, text=True)
        self.next_id = 0
        self.request("initialize", {"protocolVersion": PROTOCOL, "capabilities": {},
                                    "clientInfo": {"name": "trustloop-cora-bridge", "version": "0.1"}})
        self.notify("notifications/initialized")

    def notify(self, method, params=None):
        msg = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            msg["params"] = params
        self.proc.stdin.write(json.dumps(msg) + "\n")
        self.proc.stdin.flush()

    def request(self, method, params):
        self.next_id += 1
        rid = self.next_id
        self.proc.stdin.write(json.dumps({"jsonrpc": "2.0", "id": rid, "method": method, "params": params}) + "\n")
        self.proc.stdin.flush()
        while True:
            line = self.proc.stdout.readline()
            if not line:
                sys.exit(f"cora mcp exited before answering {method}")
            msg = json.loads(line)
            if msg.get("id") == rid:
                if "error" in msg:
                    sys.exit(f"{method} failed: {msg['error']}")
                return msg["result"]

    def call(self, tool, args):
        result = self.request("tools/call", {"name": tool, "arguments": args})
        text = "\n".join(c.get("text", "") for c in result.get("content", []) if c.get("type") == "text")
        if result.get("isError"):
            sys.exit(f"{tool} returned an error: {text}")
        return text

    def close(self):
        self.proc.terminate()


def read(path):
    with open(path) as fh:
        return fh.read()


def compact_prepare(text, skip_system_prompt):
    """Render a review_prepare result as plain text with only the fields a reviewer needs."""
    import hashlib
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return text  # not JSON: print as is rather than hide anything
    system = data.get("system_prompt", "")
    digest = hashlib.sha256(system.encode()).hexdigest()[:16]
    out = [f"valid_files: {', '.join(data.get('valid_files', []))}",
           f"untrusted_data_notice: {data.get('untrusted_data_notice', '')}",
           "deterministic_findings (already found; do not repeat them):"]
    for f in data.get("deterministic_findings", []):
        out.append(f"  - {f.get('severity')} {f.get('file')}:{f.get('line')} {f.get('title')}")
    if not data.get("deterministic_findings"):
        out.append("  (none)")
    out.append("response_schema: " + json.dumps(data.get("response_schema"), separators=(",", ":")))
    if skip_system_prompt:
        out.append(f"system_prompt: unchanged reviewer instructions, sha256 {digest} (compare with the first round)")
    else:
        out += [f"===== system_prompt (sha256 {digest}) =====", system]
    out += ["===== user_prompt =====", data.get("user_prompt", "")]
    return "\n".join(out)


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return
    s = Session()
    try:
        cmd = argv[1]
        if cmd == "list":
            for tool in s.request("tools/list", {})["tools"]:
                print(f"{tool['name']}: {tool.get('description', '').splitlines()[0]}")
        elif cmd == "call":
            print(s.call(argv[2], json.loads(argv[3]) if len(argv) > 3 else {}))
        elif cmd == "prepare":
            result = s.call("cora.review_prepare", {"diff": read(argv[2])})
            if "--compact" in argv[3:]:
                result = compact_prepare(result, "--skip-system-prompt" in argv[3:])
            print(result)
        elif cmd == "finalize":
            print(s.call("cora.review_finalize", {"diff": read(argv[2]), "issues": json.loads(read(argv[3]))}))
        else:
            sys.exit(f"unknown command {cmd!r}; see --help")
    finally:
        s.close()


if __name__ == "__main__":
    main(sys.argv)
