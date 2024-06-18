def get_file_paths_in_dir(directory):
    import os
    # Klasördeki dosyaları toplamak için boş bir liste oluştur
    file_paths = []

    # Belirtilen klasördeki tüm dosyaları döngüye al
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        
        # Dosya yolunun bir dosyaya işaret edip etmediğini kontrol et
        if os.path.isfile(file_path):
            file_paths.append(file_path)  # Dosya ismini listeye ekle
            
    return file_paths