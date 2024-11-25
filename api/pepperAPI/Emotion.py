# -*- coding: utf-8 -*-
import sys
import numpy as np
import cv2
import subprocess
from naoqi import ALProxy
import time
import boto3
import json
import matplotlib.pyplot as plt

# Configuración del cliente de AWS Rekognition
rekognition_client = boto3.client('rekognition', region_name='eu-west-1')
video_client = None
emotions = []  # Declarar la lista global para almacenar las emociones detectadas

def generate_pie_chart(emotions):
    emotion_counts = {}
    for emotion in emotions:
        emotion_name = emotion[0]
        if emotion_name in emotion_counts:
            emotion_counts[emotion_name] += 1
        else:
            emotion_counts[emotion_name] = 1

    labels = emotion_counts.keys()
    sizes = emotion_counts.values()

    plt.figure(figsize=(10, 7))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Emotion Distribution')
    plt.show()


def emotion_recognition(pepper_ip):
    global video_client  # Declarar video_client como global
    global emotions  # Declarar emotions como global

    # Conexión a Pepper
    video_proxy = ALProxy("ALVideoDevice", pepper_ip, 9559)

    # Configuración de la cámara de Pepper
    resolution = 2  # Resolución 640x480
    color_space = 13  # ColorSpace RGB
    fps = 30  # Frames por segundo

    def subscribe_camera():
        return video_proxy.subscribeCamera("VideoCapture", 0, resolution, color_space, fps)

    video_client = subscribe_camera()

    last_recognition_time = 0  # Inicializar el temporizador
    retry_count = 0  # Contador de reintentos
    max_retries = 5  # Límite máximo de reintentos

    detected_emotion = None
    emotion_confidence = 0

    try:
        while True:
            # Capturar fotograma de la cámara de Pepper
            image_data = video_proxy.getImageRemote(video_client)
            
            if image_data is None:
                print("No se pudo obtener la imagen desde la cámara de Pepper. Reintentando...")
                retry_count += 1
                if retry_count >= max_retries:
                    print("Se alcanzó el límite máximo de reintentos. Saliendo...")
                    break
                video_proxy.unsubscribe(video_client)
                video_client = subscribe_camera()
                continue

            # Restablecer el contador de reintentos si se obtiene la imagen correctamente
            retry_count = 0

            # Obtener los datos de la imagen
            width = image_data[0]
            height = image_data[1]
            array = np.frombuffer(image_data[6], dtype=np.uint8).reshape((height, width, 3))

            # Convertir la imagen a formato RGB
            rgb_frame = cv2.cvtColor(array, cv2.COLOR_BGR2RGB)

            # Realizar la detección de emociones cada 1 segundo
            current_time = time.time()
            if current_time - last_recognition_time >= 1:
                last_recognition_time = current_time

                # Codificar la imagen en formato JPEG
                _, jpeg_image = cv2.imencode('.jpg', rgb_frame)
                image_bytes = jpeg_image.tobytes()

                # Detectar rostros y emociones usando Rekognition
                try:
                    response = rekognition_client.detect_faces(
                        Image={'Bytes': image_bytes},
                        Attributes=['ALL']
                    )
                    face_details = response.get('FaceDetails', [])

                    # Procesar detalles de las caras detectadas
                    for face_detail in face_details:
                        # Obtener las coordenadas del rostro
                        box = face_detail['BoundingBox']
                        left = int(box['Left'] * width)
                        top = int(box['Top'] * height)
                        right = left + int(box['Width'] * width)
                        bottom = top + int(box['Height'] * height)

                        # Dibujar un rectángulo alrededor del rostro
                        cv2.rectangle(array, (left, top), (right, bottom), (0, 255, 0), 2)

                        # Obtener la emoción principal
                        detected_emotion = max(face_detail['Emotions'], key=lambda x: x['Confidence'])
                        emotion_type = detected_emotion['Type']
                        emotion_confidence = detected_emotion['Confidence']

                        # Guardar la emoción detectada en la lista global
                        emotions.append((emotion_type, emotion_confidence))

                except Exception as e:
                    print("Error al detectar emociones: {}".format(e))

            # Mostrar el texto con la emoción detectada y su confiabilidad
            if detected_emotion:
                text = "{} ({:.2f})".format(emotion_type, emotion_confidence)
                cv2.putText(array, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Mostrar el fotograma con el rostro y la emoción
            cv2.imshow('Emotion Recognition', array)

            # Romper el bucle si se presiona la tecla 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                video_proxy.unsubscribe(video_client)
                cv2.destroyAllWindows()
                generate_pie_chart(emotions)
                break

    finally:
        # Liberar el cliente de la cámara y cerrar las ventanas
        video_proxy.unsubscribe(video_client)
        cv2.destroyAllWindows()

def unsubscribe_camera(pepper_ip):
    global video_client  # Declarar video_client como global
    video_proxy = ALProxy("ALVideoDevice", pepper_ip, 9559)
    video_proxy.unsubscribe(video_client)