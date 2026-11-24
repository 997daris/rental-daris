class Kendaraan:
    # Class attribute untuk menghitung total unit kendaraan yang dibuat
    total_unit = 0

    def __init__(self, plat_nomor: str, merek: str, tarif_harian: int, tersedia: bool = True):
        self.plat_nomor = plat_nomor
        self.merek = merek
        self.tersedia = tersedia
        # Encapsulation: atribut privat diawali __
        self.__tarif_harian = 0

        # Memanggil setter saat inisialisasi agar validasi tarif aktif
        self.tarif_harian = tarif_harian

        Kendaraan.total_unit += 1

    # Getter & Setter untuk tarif_harian
    @property
    def tarif_harian(self) -> int:
        return self.__tarif_harian

    @tarif_harian.setter
    def tarif_harian(self, tarif: int):
        if tarif <= 0:
            raise ValueError("Tarif harian harus lebih dari 0.")
        self.__tarif_harian = tarif

    # Instance method: mengubah status kendaraan saat disewa
    def sewa(self) -> bool:
        if not self.tersedia:
            return False
        self.tersedia = False
        return True

    # Instance method: mengembalikan status kendaraan setelah selesai disewa
    def kembalikan(self):
        self.tersedia = True

    # Class method: menampilkan total kendaraan terdaftar
    @classmethod
    def info_total_unit(cls) -> str:
        return f"Total kendaraan terdaftar di sistem: {cls.total_unit}"

    # Static method: menghitung biaya sewa berdasarkan tarif dan jumlah hari
    @staticmethod
    def hitung_biaya(tarif: int, hari: int) -> int:
        if hari <= 0:
            raise ValueError("Jumlah hari sewa minimal 1 hari.")
        return tarif * hari


class LayananRental:
    def __init__(self, nama_rental: str):
        self.nama_rental = nama_rental
        self.armada = []  # List of Kendaraan
        self.riwayat_sewa = []  # List of dict

    # Instance method: menambahkan kendaraan ke armada
    def tambah_kendaraan(self, kendaraan: Kendaraan):
        self.armada.append(kendaraan)
        print(f"[OK] {kendaraan.merek} ({kendaraan.plat_nomor}) masuk armada {self.nama_rental}.")

    # Instance method: memproses penyewaan kendaraan
    def proses_sewa(self, penyewa: str, plat_nomor: str, hari: int):
        for unit in self.armada:
            if unit.plat_nomor == plat_nomor:
                if unit.sewa():
                    total_biaya = Kendaraan.hitung_biaya(unit.tarif_harian, hari)
                    self.riwayat_sewa.append({
                        "penyewa": penyewa,
                        "plat": unit.plat_nomor,
                        "merek": unit.merek,
                        "hari": hari,
                        "total": total_biaya,
                        "status": "Sedang Disewa"
                    })
                    print(
                        f"[SEWA] {penyewa} menyewa {unit.merek} ({unit.plat_nomor}) "
                        f"selama {hari} hari. Total: Rp{total_biaya:,}".replace(",", ".")
                    )
                else:
                    print(f"[GAGAL] {unit.merek} ({unit.plat_nomor}) sedang tidak tersedia.")
                return
        print(f"[GAGAL] Kendaraan dengan plat '{plat_nomor}' tidak ditemukan.")

    # Instance method: memproses pengembalian kendaraan
    def proses_kembali(self, plat_nomor: str):
        for data in self.riwayat_sewa:
            if data["plat"] == plat_nomor and data["status"] == "Sedang Disewa":
                data["status"] = "Selesai"
                for unit in self.armada:
                    if unit.plat_nomor == plat_nomor:
                        unit.kembalikan()
                        print(f"[KEMBALI] {unit.merek} ({plat_nomor}) telah dikembalikan dan tersedia lagi.")
                        return
        print(f"[GAGAL] Tidak ada transaksi aktif untuk plat '{plat_nomor}'.")

    # Instance method: menampilkan daftar armada
    def tampilkan_armada(self):
        print(f"\n=== ARMADA {self.nama_rental.upper()} ===")
        for unit in self.armada:
            status_teks = "Tersedia" if unit.tersedia else "Disewa"
            print(
                f"[{unit.plat_nomor}] {unit.merek} | "
                f"Tarif: Rp{unit.tarif_harian:,}/hari | Status: {status_teks}".replace(",", ".")
            )
        print()


# --- Eksekusi / Pembuatan Object ---
if __name__ == "__main__":
    # Membuat object dari class Kendaraan
    mobil_1 = Kendaraan("A 1234 XY", "Toyota Avanza", 350000)
    motor_1 = Kendaraan("A 5678 ZZ", "Honda Vario 160", 120000)

    # Membuat object dari class LayananRental
    rental = LayananRental("Banten Jaya Rental")
    rental.tambah_kendaraan(mobil_1)
    rental.tambah_kendaraan(motor_1)

    # Menguji setter melalui @property
    motor_1.tarif_harian = 135000
    print(f"Tarif baru {motor_1.merek}: Rp{motor_1.tarif_harian:,}/hari".replace(",", "."))

    # Proses sewa dan pengembalian
    rental.proses_sewa("Fajar", "A 1234 XY", 3)
    rental.tampilkan_armada()

    rental.proses_kembali("A 1234 XY")
    rental.tampilkan_armada()

    # Memanggil class method
    print(Kendaraan.info_total_unit())