KBK = []

KL_M = []
for n in range(0, 200):
    KL_M.append(f"M {n + 1}")
KL_M = tuple(KL_M)

KL_K = []
for n in range(0, 16):
    KL_K.append(f"K {n + 1}")
KL_K = tuple(KL_K)

KL_B1 = []
for n in range(0, 50):
    KL_B1.append(f"BA1 {n + 1}")
KL_B1 = tuple(KL_B1)

KL_B2 = []
for n in range(0, 50):
    KL_B2.append(f"BA2 {n + 1}")
KL_B2 = tuple(KL_B2)

KL_B3 = []
for n in range(0, 50):
    KL_B3.append(f"BA3 {n + 1}")
KL_B3 = tuple(KL_B3)

KL_B4 = []
for n in range(0, 50):
    KL_B4.append(f"BA4 {n + 1}")
KL_B4 = tuple(KL_B4)

KL_MB1 = []
for n in range(0, 25):
    KL_MB1.append(f"MB1 {n + 1}")
KL_MB1 = tuple(KL_MB1)

KL_MB2 = []
for n in range(0, 25):
    KL_MB2.append(f"MB2 {n + 1}")
KL_MB2 = tuple(KL_MB2)

KL_MB3 = []
for n in range(0, 25):
    KL_MB3.append(f"MB3 {n + 1}")
KL_MB3 = tuple(KL_MB3)

KL_MB4 = []
for n in range(0, 25):
    KL_MB4.append(f"MB4 {n + 1}")
KL_MB4 = tuple(KL_MB4)

KL_C = []
for n in range(0, 10):
    KL_C.append(f"C {n + 1}")
KL_C = tuple(KL_C)
KL_CH = []
for n in range(0, 100):
    KL_CH.append(f"CH {n + 1}")
KL_C = tuple(KL_C)

p6509 = []
for n in range(7, -1, -1):
    p6509.append(f"P 2.{n}")
    p6509.append(f"P 5.{n}")
for n in range(7, -1, -1):
    p6509.append(f"P 1.{n}")
    p6509.append(f"P 4.{n}")
for n in range(7, -1, -1):
    p6509.append(f"P 0.{n}")
    p6509.append(f"P 3.{n}")
p6509.append("+5")
p6509.append("GN1")
for n in range(7, -1, -1):
    p6509.append(f"P 8.{n}")
    p6509.append(f"P 11.{n}")
for n in range(7, -1, -1):
    p6509.append(f"P 7.{n}")
    p6509.append(f"P 10.{n}")
for n in range(7, -1, -1):
    p6509.append(f"P 6.{n}")
    p6509.append(f"P 9.{n}")
p6509.append("+5")
p6509.append("GN2")
p6509 = tuple(p6509)

KBK.append(KL_M)
KBK.append(KL_K)
KBK.append(KL_B1)
KBK.append(KL_B2)
KBK.append(KL_B3)
KBK.append(KL_B4)
KBK.append(KL_MB1)
KBK.append(KL_MB2)
KBK.append(KL_MB3)
KBK.append(KL_MB4)
KBK.append(KL_C)
KBK.append(KL_CH)
KBK.append(p6509)


class Kblck():
    def __init__(self):
        self.nodes = []

    def add_kbk(self):
        KL_M = []
        for n in range(0, 200):
            KL_M.append(f"M {n + 1}")
        KL_M = tuple(KL_M)

        KL_K = []
        for n in range(0, 16):
            KL_K.append(f"K {n + 1}")
        KL_K = tuple(KL_K)

        KL_B1 = []
        for n in range(0, 50):
            KL_B1.append(f"BA1 {n + 1}")
        KL_B1 = tuple(KL_B1)

        KL_B2 = []
        for n in range(0, 50):
            KL_B2.append(f"BA2 {n + 1}")
        KL_B2 = tuple(KL_B2)

        KL_B3 = []
        for n in range(0, 50):
            KL_B3.append(f"BA3 {n + 1}")
        KL_B3 = tuple(KL_B3)

        KL_B4 = []
        for n in range(0, 50):
            KL_B4.append(f"BA4 {n + 1}")
        KL_B4 = tuple(KL_B4)

        KL_MB1 = []
        for n in range(0, 25):
            KL_MB1.append(f"MB1 {n + 1}")
        KL_MB1 = tuple(KL_MB1)

        KL_MB2 = []
        for n in range(0, 25):
            KL_MB2.append(f"MB2 {n + 1}")
        KL_MB2 = tuple(KL_MB2)

        KL_MB3 = []
        for n in range(0, 25):
            KL_MB3.append(f"MB3 {n + 1}")
        KL_MB3 = tuple(KL_MB3)

        KL_MB4 = []
        for n in range(0, 25):
            KL_MB4.append(f"MB4 {n + 1}")
        KL_MB4 = tuple(KL_MB4)

    def add_6509(self):
        pass

    def add_2568(self):
        pass

    def add_2569(self):
        pass


def print_kb(kb):
    for klemnik in kb:
        for node in klemnik:
            print(node)


if __name__ == "__main__":
    print(KBK)
