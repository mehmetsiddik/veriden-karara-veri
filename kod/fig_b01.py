# Bölüm 1 şekil verileri: üstel evrenden örneklem ortalamalarının dağılımı
import numpy as np
from pathlib import Path
out = Path(__file__).resolve().parent.parent / "figures" / "data"
rng = np.random.default_rng(1)
for n in [1, 5, 30]:
    m = rng.exponential(1.0, size=(20000, n)).mean(1)
    edges = np.linspace(0, 4, 41)
    h, e = np.histogram(m, bins=edges, density=True)
    with open(out / f"b01_ornekleme_n{n}.dat", "w") as f:
        f.write("x y\n")
        for xi, yi in zip(e[:-1], h):
            f.write(f"{xi:.2f} {yi:.4f}\n")
        f.write(f"{e[-1]:.2f} 0\n")
    print(n, m.mean().round(4), m.std(ddof=1).round(4), (1/np.sqrt(n)).round(4))
