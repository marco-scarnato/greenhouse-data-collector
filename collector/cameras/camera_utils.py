import cv2
import os
import db_utils

def list_available_cameras(max_index=10):
    """ Trova e restituisce un elenco delle webcam disponibili. """
    available_cameras = []
    for i in range(max_index):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available_cameras.append(i)
            cap.release()
    return available_cameras

def take_a_photo(photo_id, status="Healty", plant_name="basil", camera_index=0):
    """ Scatta una foto dalla webcam specificata e la salva nella cartella indicata. """

    # Inizializza la webcam con l'indice scelto
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print(f"Errore: impossibile aprire la webcam con indice {camera_index}.")
        return

    ret, frame = cap.read()
    if not ret:
        print("Errore: impossibile catturare il frame.")
    else:
        # Mostra il video in tempo reale
        cv2.imshow("Webcam", frame)
        cv2.waitKey(500)  # Aspetta mezzo secondo per evitare schermate nere

        # Invia l'immagine direttamente al database
        _, buffer = cv2.imencode('.jpg', frame)  # Converte il frame in un buffer di immagine
        photo_bytes = buffer.tobytes()  # Converte l'immagine in bytes

        db_utils.post_photo(photo_id, photo_bytes, status, plant_name)
        print(f"Foto {photo_id} inviata al database con successo.")


    # Rilascia la webcam e chiude la finestra
    cap.release()
    cv2.destroyAllWindows()

def save_photo_to_file(photo_data, output_path):
    """Salva i dati binari della foto in un file."""
    try:
        with open(output_path, 'wb') as file:
            file.write(photo_data)
        print(f"Foto salvata con successo in: {output_path}")
        return True
    except Exception as e:
        print(f"Errore durante il salvataggio della foto: {e}")
        return False
