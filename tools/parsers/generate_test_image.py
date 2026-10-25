from PIL import Image
import piexif

# Criar uma imagem simples 100x100 em branco
img = Image.new('RGB', (100, 100), color = (73, 109, 137))

# Metadados EXIF simulando coordenadas GPS (Luanda, Angola: Lat -8.838333, Lon 13.234444)
zeroth_ifd = {
    piexif.ImageIFD.Make: "Apple",
    piexif.ImageIFD.Model: "iPhone 15 Pro",
    piexif.ImageIFD.Software: "iOS 17.5.1"
}

exif_ifd = {
    piexif.ExifIFD.DateTimeOriginal: "2026-09-30 14:20:00"
}

# GPS: 8°50'18.0"S 13°14'04.0"E -> Grau, Min, Seg (Racionais: num, den)
gps_ifd = {
    piexif.GPSIFD.GPSLatitudeRef: "S",
    piexif.GPSIFD.GPSLatitude: ((8, 1), (50, 1), (1800, 100)),
    piexif.GPSIFD.GPSLongitudeRef: "E",
    piexif.GPSIFD.GPSLongitude: ((13, 1), (14, 1), (400, 100))
}

exif_dict = {"0th": zeroth_ifd, "Exif": exif_ifd, "GPS": gps_ifd}
exif_bytes = piexif.dump(exif_dict)

# Gravar imagem de teste
caminho_saida = "casos/caso_01_operacao_sombra_digital/raw_evidence/evidencia_foto_suspeito.jpg"
img.save(caminho_saida, exif=exif_bytes)
print(f"[+] Imagem de teste criada com EXIF GPS em: {caminho_saida}")
