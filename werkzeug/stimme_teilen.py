"""Teilt eine Sammel-Sprachaufnahme (alle Reels einer Woche in einem vidIQ-Auftrag) an den längsten Pausen.

Aufruf:
  python werkzeug/stimme_teilen.py stimmen/2026-10-26-woche.mp3 5 stimmen/2026-10-26-

Schreibt <praefix>1.mp3 ... <praefix>N.mp3 (in der Reihenfolge der Texte) und gibt die Länge jedes Teils aus.
Bricht ab, wenn die Pausen zwischen den Texten nicht klar länger sind als die Pausen innerhalb der Texte.
"""
import re, subprocess, sys


def main():
    quelle, n, praefix = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    r = subprocess.run(["ffmpeg", "-i", quelle, "-af", "silencedetect=noise=-35dB:d=0.3", "-f", "null", "-"],
                       capture_output=True, text=True)
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r.stderr)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r.stderr)]
    dauer = float(re.search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr).group(3)) + \
        60 * int(re.search(r"Duration: (\d+):(\d+)", r.stderr).group(2))
    pausen = [(e - s, s, e) for s, e in zip(starts, ends) if s > 0.5 and e < dauer - 0.3]
    if len(pausen) < n - 1:
        raise SystemExit(f"Nur {len(pausen)} Pausen gefunden, {n - 1} nötig.")
    pausen.sort(reverse=True)
    trenner, rest = pausen[:n - 1], pausen[n - 1:]
    if rest and min(p[0] for p in trenner) < max(p[0] for p in rest) + 0.25:
        raise SystemExit("Pausen zwischen den Texten sind nicht klar länger als innerhalb. Nicht aufteilen.")
    trenner.sort(key=lambda p: p[1])
    # Jeder Teil beginnt kurz vor dem ersten Wort und endet kurz nach dem letzten
    anfang = [0.0] + [max(p[2] - 0.05, 0) for p in trenner]
    ende = [p[1] + 0.15 for p in trenner] + [dauer]
    for i in range(n):
        a, b = anfang[i], ende[i]
        ziel = f"{praefix}{i + 1}.mp3"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", quelle, "-ss", f"{a:.3f}", "-to", f"{b:.3f}",
                        "-c:a", "libmp3lame", "-b:a", "192k", ziel], check=True)
        print(f"{ziel}: {a:.2f} bis {b:.2f} s, Laenge {b - a:.2f} s")


if __name__ == "__main__":
    main()
