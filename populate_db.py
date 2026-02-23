from dotenv import load_dotenv

load_dotenv()

from app.database import SessionLocal, engine, Base
from app.models import Recinto, Evento
from datetime import date, timedelta
import random

Base.metadata.create_all(bind=engine)


def populate():
    db = SessionLocal()

    try:
        if db.query(Recinto).count() > 0:
            print("Ya existen datos")
            print(f"Recintos: {db.query(Recinto).count()}")
            print(f"Eventos: {db.query(Evento).count()}")
            return

        print("=== POBLANDO BASE DE DATOS ===\n")

        recintos_data = [
            {"nombre": "Estadio Bernabeu", "ciudad": "Madrid", "capacidad": 85000},
            {"nombre": "Camp Nou", "ciudad": "Barcelona", "capacidad": 80000},
            {"nombre": "Wizink Center", "ciudad": "Madrid", "capacidad": 21000},
            {"nombre": "Palau Sant Jordi", "ciudad": "Barcelona", "capacidad": 10000},
            {"nombre": "Estadio La Cartuja", "ciudad": "Sevilla", "capacidad": 65000},
            {"nombre": "Teatro Real", "ciudad": "Madrid", "capacidad": 20000},
        ]

        recintos = []
        for data in recintos_data:
            recinto = Recinto(**data)
            db.add(recinto)
            recintos.append(recinto)
            print(f"Recinto: {data['nombre']}")

        db.commit()
        for r in recintos:
            db.refresh(r)

        print("")

        eventos_data = [
            {"nombre": "Concierto Coldplay", "precio": 120.00, "dias": 30},
            {"nombre": "Final Champions", "precio": 350.00, "dias": 60},
            {"nombre": "Opera Italiana", "precio": 150.00, "dias": 45},
            {"nombre": "Festival Primavera", "precio": 85.00, "dias": 90},
            {"nombre": "Ballet Ruso", "precio": 75.00, "dias": 15},
            {"nombre": "Concierto The musica Band", "precio": 95.00, "dias": 25},
        ]

        for data in eventos_data:
            recinto = random.choice(recintos)
            tickets = random.randint(100, int(recinto.capacidad * 0.5))

            evento = Evento(
                nombre=data["nombre"],
                fecha=date.today() + timedelta(days=data["dias"]),
                precio=data["precio"],
                tickets_vendidos=tickets,
                recinto_id=recinto.id
            )
            db.add(evento)
            print(f"Evento: {data['nombre']} en {recinto.nombre}")

        db.commit()


    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    populate()